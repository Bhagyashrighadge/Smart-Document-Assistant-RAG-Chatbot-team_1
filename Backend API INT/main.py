"""
FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from fastapi.middleware.gzip import GZIPMiddleware
    HAS_GZIP = True
except ImportError:
    HAS_GZIP = False
import logging
import os
from dotenv import load_dotenv

from api.routes import router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="BhashaSetu - Multilingual Smart Document Assistant",
    description="RAG-based document question answering system with multilingual support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZIP compression middleware if available
if HAS_GZIP:
    app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Include routers
app.include_router(router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BhashaSetu - Multilingual Smart Document Assistant",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    logger.info("Starting BhashaSetu application...")
    
    # Verify Gemini API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not set in environment")
    else:
        logger.info("Gemini API key loaded successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    logger.info("Shutting down BhashaSetu application...")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
