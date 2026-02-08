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
from services.deepseek_service import DeepSeekService
from services.translator import TranslatorService
from services.language_detector import is_response_in_language, validate_language_strict, log_language_decision
from services.mock_responses import enable_mock_mode
from models.session_store import session_store, ChatMessage as StoredChatMessage

router = APIRouter()

# Global instances
pdf_processor = PDFProcessor()
translator_service = TranslatorService()
deepseek_service = None  # Lazy initialized

# Session-specific RAG pipelines
rag_pipelines = {}


def get_deepseek_service():
    """Get or create DeepSeek service"""
    global deepseek_service
    if deepseek_service is None:
        try:
            deepseek_service = DeepSeekService()
        except ValueError as e:
            logging.error(f"Failed to initialize DeepSeek service: {str(e)}")
            raise
    return deepseek_service


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    try:
        service = get_deepseek_service()
        is_connected = service.test_connection()
        
        if is_connected:
            return HealthResponse(
                status="healthy",
                message="All services operational (DeepSeek API connected)"
            )
        else:
            return HealthResponse(
                status="degraded",
                message="DeepSeek API connection failed"
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
        # STEP 1: Log the incoming request
        logging.info("=" * 60)
        logging.info("ASK-QUESTION ENDPOINT CALLED")
        logging.info("=" * 60)
        logging.info(f"[QUESTION] {request.question}")
        logging.info(f"[LANGUAGE] {request.language}")
        logging.info(f"[SESSION_ID] {request.session_id}")
        
        # STEP 2: Get RAG pipeline for session
        rag_pipeline = rag_pipelines.get(request.session_id)
        if not rag_pipeline:
            logging.error(f"RAG pipeline not found for session: {request.session_id}")
            raise HTTPException(
                status_code=500,
                detail="RAG pipeline not initialized for this session"
            )
        
        # STEP 3: Retrieve context from documents
        logging.info("[STEP 1] Retrieving context from RAG pipeline...")
        try:
            context = rag_pipeline.get_context(request.question, top_k=3)
            logging.info(f"[CONTEXT] Retrieved {len(context)} characters")
            logging.info(f"[CONTEXT_PREVIEW] {context[:200]}..." if len(context) > 200 else f"[CONTEXT_PREVIEW] {context}")
        except Exception as e:
            logging.error(f"[ERROR] Failed to retrieve context: {str(e)}")
            raise
        
        # STEP 4: Validate context
        if not context or context.strip() == "":
            logging.warning("[WARNING] No relevant context found for question")
            return QuestionResponse(
                success=False,
                answer="",
                original_answer="",
                language=request.language,
                message="No relevant information found in the document."
            )
        
        # STEP 5: Initialize DeepSeek service
        logging.info("[STEP 2] Initializing DeepSeek service...")
        try:
            service = get_deepseek_service()
            logging.info("[SUCCESS] DeepSeek service initialized")
        except Exception as e:
            logging.error(f"[ERROR] Failed to initialize DeepSeek service: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"API key not configured or service initialization failed: {str(e)}"
            )
        
        # STEP 6: Generate response using DeepSeek API
        logging.info("[STEP 3] Calling DeepSeek API for response generation...")
        logging.info(f"[API_KEY_LOADED] {bool(service.api_key)}")
        
        try:
            original_answer = service.generate_response(
                prompt=request.question,
                context=context,
                language=request.language
            )
            
            if not original_answer:
                logging.error("[ERROR] DeepSeek API returned None/empty response")
                raise HTTPException(
                    status_code=500,
                    detail="Failed to generate response from DeepSeek API. Please check API key and connection."
                )
            
            logging.info(f"[SUCCESS] Generated answer with {len(original_answer)} characters")
            logging.info(f"[ANSWER_PREVIEW] {original_answer[:200]}..." if len(original_answer) > 200 else f"[ANSWER_PREVIEW] {original_answer}")
            
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"[ERROR] DeepSeek API call failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate response from DeepSeek API: {str(e)}"
            )
        
        # STEP 7: Strict Language Validation and Enforcement
        logging.info("[STEP 4] Validating response language...")
        answer = original_answer
        
        # Check if response is in the requested language
        is_valid, detected_language, confidence = is_response_in_language(original_answer, request.language)
        
        logging.info(f"[LANGUAGE_VALIDATION] Requested: {request.language}")
        logging.info(f"[LANGUAGE_VALIDATION] Detected: {detected_language}")
        logging.info(f"[LANGUAGE_VALIDATION] Confidence: {confidence:.2%}")
        logging.info(f"[LANGUAGE_VALIDATION] Status: {'✓ VALID' if is_valid else '✗ INVALID'}")
        
        # Log language decision for debugging
        log_language_decision(
            language=request.language,
            context_size=len(context),
            question=request.question,
            detected_in_response=detected_language,
            is_valid=is_valid
        )
        
        # If validation failed but we got a response, log warning but use it
        if not is_valid:
            logging.warning(f"[WARNING] Response may not be in requested language ({request.language})")
            logging.warning(f"[WARNING] Detected language: {detected_language}")
            # Note: We still use the response as the model tried its best
        
        logging.info(f"[LANGUAGE_FINAL] Answer language: {request.language}")
        
        # STEP 8: Store in chat history
        logging.info("[STEP 5] Storing in chat history...")
        try:
            session_store.add_message(request.session_id, "user", request.question)
            session_store.add_message(request.session_id, "assistant", original_answer)
            session_store.update_session(request.session_id, language=request.language)
            logging.info("[SUCCESS] Chat history updated")
        except Exception as e:
            logging.warning(f"[WARNING] Failed to update chat history: {str(e)}")
        
        # STEP 9: Return success response
        logging.info("[FINAL] Returning successful response")
        logging.info("=" * 60)
        
        return QuestionResponse(
            success=True,
            answer=answer,
            original_answer=original_answer,
            language=request.language
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"[FATAL] Unexpected error in ask_question: {str(e)}")
        logging.exception("Full traceback:")
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
