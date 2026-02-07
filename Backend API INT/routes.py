"""
API Routes - Define all API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Optional
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path for absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.schemas import (
    UploadResponse, QuestionRequest, QuestionResponse,
    TranslateRequest, TranslateResponse, HealthResponse, SessionInfoResponse, ChatMessage
)
from api.utils import save_upload_file, cleanup_temp_file, validate_pdf_file
from services.pdf_processor import PDFProcessor
from services.rag_pipeline import RAGPipeline
from services.gemini_service import GeminiService
from services.translator import TranslatorService
from models.session_store import session_store, ChatMessage as StoredChatMessage

router = APIRouter()

# Global instances
pdf_processor = PDFProcessor()
translator_service = TranslatorService()
gemini_service = None  # Lazy initialized

# Session-specific RAG pipelines
rag_pipelines = {}


def get_gemini_service():
    """Get or create Gemini service"""
    global gemini_service
    if gemini_service is None:
        try:
            gemini_service = GeminiService()
        except ValueError as e:
            logging.error(f"Failed to initialize Gemini service: {str(e)}")
            raise
    return gemini_service


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    try:
        service = get_gemini_service()
        is_connected = service.test_connection()
        
        if is_connected:
            return HealthResponse(
                status="healthy",
                message="All services operational (Gemini API connected)"
            )
        else:
            return HealthResponse(
                status="degraded",
                message="Gemini API connection failed"
            )
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            message=f"Error: {str(e)}"
        )


@router.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process PDF file
    
    Args:
        file: PDF file to upload
        
    Returns:
        Upload response with session ID
    """
    # Validate file
    if not validate_pdf_file(file):
        raise HTTPException(
            status_code=400,
            detail="Invalid file. Please upload a PDF file."
        )
    
    # Create session
    session_id = session_store.create_session()
    
    temp_file_path = None
    try:
        # Save uploaded file
        temp_file_path = await save_upload_file(file)
        if not temp_file_path:
            raise HTTPException(
                status_code=500,
                detail="Failed to save uploaded file"
            )
        
        # Extract text from PDF
        text = pdf_processor.extract_text(temp_file_path)
        if not text:
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text from PDF. File may be empty or corrupted."
            )
        
        # Clean text
        text = pdf_processor.clean_text(text)
        
        # Chunk text
        chunks = pdf_processor.chunk_text(text)
        
        # Create RAG pipeline for this session
        rag_pipeline = RAGPipeline()
        rag_pipeline.create_collection(f"session_{session_id}")
        rag_pipeline.add_documents(chunks)
        
        # Store in RAG pipelines
        rag_pipelines[session_id] = rag_pipeline
        
        # Update session
        session_store.update_session(
            session_id,
            document_name=file.filename,
            document_text=text
        )
        
        return UploadResponse(
            success=True,
            session_id=session_id,
            message=f"Successfully processed '{file.filename}'",
            document_name=file.filename
        )
    
    except HTTPException:
        # Delete session on error
        session_store.delete_session(session_id)
        if session_id in rag_pipelines:
            del rag_pipelines[session_id]
        raise
    
    except Exception as e:
        # Delete session on error
        session_store.delete_session(session_id)
        if session_id in rag_pipelines:
            del rag_pipelines[session_id]
        raise HTTPException(
            status_code=500,
            detail=f"Error processing PDF: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_file_path:
            cleanup_temp_file(temp_file_path)


@router.post("/ask-question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about the uploaded document
    
    Args:
        request: Question request with session ID and question
        
    Returns:
        Answer from the document
    """
    # Validate session
    session = session_store.get_session(request.session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found or expired"
        )
    
    # Validate language
    if request.language not in ["en", "hi", "mr"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid language. Supported: en, hi, mr"
        )
    
    try:
        # Get RAG pipeline for session
        rag_pipeline = rag_pipelines.get(request.session_id)
        if not rag_pipeline:
            raise HTTPException(
                status_code=500,
                detail="RAG pipeline not initialized for this session"
            )
        
        # Retrieve context from documents
        logging.info(f"Retrieving context for question: {request.question}")
        context = rag_pipeline.get_context(request.question, top_k=3)
        
        if not context:
            logging.warning(f"No relevant context found for question: {request.question}")
            return QuestionResponse(
                success=False,
                answer="",
                original_answer="",
                language=request.language,
                message="No relevant information found in the document."
            )
        
        logging.info(f"Context retrieved: {len(context)} chars")
        
        # Generate response using Gemini
        logging.info(f"Sending request to Gemini API...")
        service = get_gemini_service()
        original_answer = service.generate_response(
            prompt=request.question,
            context=context
        )
        
        if not original_answer:
            logging.error(f"Gemini API failed to generate response for question: {request.question}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate response from Gemini API"
            )
        
        logging.info(f"Generated answer: {len(original_answer)} chars")
        
        # Translate if needed
        answer = original_answer
        if request.language != "en":
            answer = translator_service.translate(original_answer, request.language)
        
        # Store in chat history
        session_store.add_message(request.session_id, "user", request.question)
        session_store.add_message(request.session_id, "assistant", original_answer)
        
        # Update language preference
        session_store.update_session(request.session_id, language=request.language)
        
        return QuestionResponse(
            success=True,
            answer=answer,
            original_answer=original_answer,
            language=request.language
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@router.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    Translate text to target language
    
    Args:
        request: Translation request
        
    Returns:
        Translated text
    """
    if request.target_language not in ["en", "hi", "mr"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid language. Supported: en, hi, mr"
        )
    
    try:
        translated = translator_service.translate(request.text, request.target_language)
        
        return TranslateResponse(
            success=True,
            original_text=request.text,
            translated_text=translated,
            target_language=request.target_language
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation error: {str(e)}"
        )


@router.get("/session/{session_id}", response_model=SessionInfoResponse)
async def get_session_info(session_id: str):
    """
    Get information about a session
    
    Args:
        session_id: Session ID
        
    Returns:
        Session information
    """
    session = session_store.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    
    try:
        chat_messages = [
            ChatMessage(
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp.isoformat()
            )
            for msg in session.chat_history
        ]
        
        return SessionInfoResponse(
            session_id=session.session_id,
            document_name=session.document_name,
            created_at=session.created_at.isoformat(),
            language=session.language,
            chat_history=chat_messages
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving session info: {str(e)}"
        )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session
    
    Args:
        session_id: Session ID
        
    Returns:
        Success status
    """
    try:
        success = session_store.delete_session(session_id)
        
        # Clean up RAG pipeline
        if session_id in rag_pipelines:
            del rag_pipelines[session_id]
        
        if success:
            return {"success": True, "message": "Session deleted"}
        else:
            raise HTTPException(
                status_code=404,
                detail="Session not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting session: {str(e)}"
        )
