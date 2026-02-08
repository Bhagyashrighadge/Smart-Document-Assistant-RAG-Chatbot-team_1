"""
Main entry point for Smart Document Assistant
Initialize and configure the application
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from common.logger import setup_logger

logger = setup_logger(__name__)

# Import main components for easy access
from pipeline import DocumentProcessingPipeline, process_document
from text_extraction import TextExtractor, extract_text
from text_preprocessing import TextPreprocessor, preprocess_text
from common.data_models import ExtractionResult, PreprocessedResult, ProcessingPipeline

logger.info("Smart Document Assistant initialized")

__version__ = "1.0.0"
__all__ = [
    "DocumentProcessingPipeline",
    "process_document",
    "TextExtractor",
    "extract_text",
    "TextPreprocessor",
    "preprocess_text",
    "ExtractionResult",
    "PreprocessedResult",
    "ProcessingPipeline",
]

if __name__ == "__main__":
    print("Smart Document Assistant - Text Processing Module")
    print(f"Version: {__version__}")
    print(f"Project Root: {PROJECT_ROOT}")
