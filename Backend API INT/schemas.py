"""
API Schemas - Request/Response models
"""
from pydantic import BaseModel
from typing import Optional, List


class UploadResponse(BaseModel):
    """Response for PDF upload"""
    success: bool
    session_id: str
    message: str
    document_name: str


class QuestionRequest(BaseModel):
    """Request for asking a question"""
    session_id: str
    question: str
    language: str = "en"  # en, hi, mr


class QuestionResponse(BaseModel):
    """Response for question"""
    success: bool
    answer: str
    original_answer: str
    language: str
    message: Optional[str] = None


class TranslateRequest(BaseModel):
    """Request for translation"""
    text: str
    target_language: str  # en, hi, mr


class TranslateResponse(BaseModel):
    """Response for translation"""
    success: bool
    original_text: str
    translated_text: str
    target_language: str


class HealthResponse(BaseModel):
    """Response for health check"""
    status: str
    message: str


class ChatMessage(BaseModel):
    """Chat message"""
    role: str
    content: str
    timestamp: Optional[str] = None


class SessionInfoResponse(BaseModel):
    """Session information"""
    session_id: str
    document_name: str
    created_at: str
    language: str
    chat_history: List[ChatMessage]
