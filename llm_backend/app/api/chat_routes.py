from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    language: str = 'en'

class ChatResponse(BaseModel):
    answer: str
    source_chunks: list

# Instantiate a default AIService (teams can inject their own)
_service = AIService()

@router.post('/chat', response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.question:
        raise HTTPException(status_code=400, detail='question is required')
    if req.language not in ('en', 'hi', 'mr'):
        raise HTTPException(status_code=400, detail='unsupported language')
    resp = _service.answer_question(req.question, req.language)
    return resp
