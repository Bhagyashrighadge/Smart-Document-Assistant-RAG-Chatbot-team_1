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
from pathlib import Path
from dotenv import load_dotenv
import sys

from api.routes import router

# Add parent directory for voice module imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Try to import voice module (optional)
try:
    from speach_module.routes import router as voice_router
    VOICE_MODULE_AVAILABLE = True
except ImportError:
    VOICE_MODULE_AVAILABLE = False
    logger_init = logging.getLogger(__name__)
    logger_init.info("Voice module not available. Install dependencies to enable: pip install -r speach_module/requirements.txt")

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

# Include voice module router if available
if VOICE_MODULE_AVAILABLE:
    app.include_router(voice_router, prefix="/api", tags=["voice"])
    logger.info("Voice module loaded successfully")


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
    
    # Initialize voice module if available
    if VOICE_MODULE_AVAILABLE:
        try:
            logger.info("Voice module is available and loaded")
        except Exception as e:
            logger.warning(f"Voice module initialization warning: {e}")


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
