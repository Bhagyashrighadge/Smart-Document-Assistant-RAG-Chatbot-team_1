from fastapi import FastAPI
from app.api.chat_routes import router as chat_router
from app.utils.logger import get_logger

logger = get_logger()

app = FastAPI(title="Smart Document Assistant - RAG Chatbot")
app.include_router(chat_router, prefix="/api")

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting app...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
