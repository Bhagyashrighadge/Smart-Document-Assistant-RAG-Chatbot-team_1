"""
REST API Interface for Document Processing
FastAPI endpoints for integration with other services
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import tempfile
from pathlib import Path

from pipeline import process_document
from common.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="Smart Document Assistant - Text Processing API",
    description="Document Extraction and Preprocessing Service",
    version="1.0.0"
)

# ==================== REQUEST/RESPONSE MODELS ====================

class ExtractionRequest(BaseModel):
    """Request model for text extraction"""
    file_path: str
    extraction_method: str = "hybrid"

class PreprocessingRequest(BaseModel):
    """Request model for text preprocessing"""
    text: str
    language: str = "en"

class ProcessingRequest(BaseModel):
    """Request model for complete processing"""
    file_path: str
    language: str = "en"
    extraction_method: str = "hybrid"

# ==================== EXTRACTION ENDPOINTS ====================

@app.post("/api/v1/extract")
async def extract(request: ExtractionRequest):
    """
    Extract text from PDF file
    
    Endpoint for: Text Extraction Module
    Integration: Returns ExtractionResult as JSON
    
    Args:
        file_path: Path to PDF file
        extraction_method: 'pypdf', 'pdfplumber', or 'hybrid'
    
    Returns:
        JSON with extracted text and metadata
    """
    try:
        from text_extraction import extract_text
        
        result = extract_text(request.file_path, method=request.extraction_method)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": result.to_dict()
            }
        )
    except Exception as e:
        logger.error(f"Extraction endpoint error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Extraction failed: {str(e)}")

@app.post("/api/v1/extract-file")
async def extract_file(file: UploadFile = File(...)):
    """
    Extract text from uploaded PDF file
    
    Args:
        file: PDF file upload
    
    Returns:
        JSON with extracted text
    """
    try:
        from text_extraction import extract_text
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
        
        try:
            result = extract_text(tmp_path)
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "data": result.to_dict()
                }
            )
        finally:
            # Clean up
            Path(tmp_path).unlink()
            
    except Exception as e:
        logger.error(f"File extraction endpoint error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Extraction failed: {str(e)}")

# ==================== PREPROCESSING ENDPOINTS ====================

@app.post("/api/v1/preprocess")
async def preprocess(request: PreprocessingRequest):
    """
    Preprocess extracted text
    
    Endpoint for: Text Preprocessing Module
    Integration: Accepts raw text, returns PreprocessedResult as JSON
    
    Args:
        text: Raw text to preprocess
        language: Target language ('en', 'hi', 'mr')
    
    Returns:
        JSON with cleaned text, sentences, tokens
    """
    try:
        from text_preprocessing import preprocess_text
        
        result = preprocess_text(request.text, language=request.language)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": result.to_dict()
            }
        )
    except Exception as e:
        logger.error(f"Preprocessing endpoint error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Preprocessing failed: {str(e)}")

# ==================== PIPELINE ENDPOINTS ====================

@app.post("/api/v1/process-full")
async def process_full(request: ProcessingRequest):
    """
    Complete document processing: Extraction + Preprocessing
    
    MAIN INTEGRATION POINT
    Combines both modules into single endpoint
    
    Args:
        file_path: Path to PDF document
        language: Target language
        extraction_method: PDF extraction method
    
    Returns:
        JSON with extraction and preprocessing results
    """
    try:
        result = process_document(
            request.file_path,
            language=request.language,
            extraction_method=request.extraction_method
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "status": result.status,
                "data": result.to_dict()
            }
        )
    except Exception as e:
        logger.error(f"Full processing endpoint error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")

@app.post("/api/v1/process-file")
async def process_file(
    file: UploadFile = File(...),
    language: str = "en"
):
    """
    Complete processing of uploaded PDF file
    
    Args:
        file: PDF file upload
        language: Target language
    
    Returns:
        JSON with complete processing results
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
        
        try:
            result = process_document(tmp_path, language=language)
            return JSONResponse(
                status_code=200,
                content={
                    "status": result.status,
                    "data": result.to_dict()
                }
            )
        finally:
            # Clean up
            Path(tmp_path).unlink()
            
    except Exception as e:
        logger.error(f"File processing endpoint error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")

# ==================== HEALTH CHECK ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Smart Document Assistant - Text Processing",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "service": "Smart Document Assistant - Text Processing API",
        "version": "1.0.0",
        "endpoints": {
            "extraction": {
                "post": "/api/v1/extract",
                "post_file": "/api/v1/extract-file"
            },
            "preprocessing": {
                "post": "/api/v1/preprocess"
            },
            "pipeline": {
                "post": "/api/v1/process-full",
                "post_file": "/api/v1/process-file"
            },
            "health": {
                "get": "/health"
            }
        }
    }

# ==================== ERROR HANDLERS ====================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
