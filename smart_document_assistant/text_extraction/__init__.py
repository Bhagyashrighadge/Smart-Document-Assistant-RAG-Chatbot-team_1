"""
Text Extraction Module Interface
Entry point for text extraction with standardized API
"""

from pathlib import Path
from typing import Optional

from text_extraction.pdf_extractor import TextExtractorFactory
from common.logger import setup_logger
from common.data_models import ExtractionResult
from config.settings import EXTRACTION_CONFIG

logger = setup_logger(__name__)

class TextExtractor:
    """
    Main interface for text extraction
    INTEGRATION POINT: Use this class to extract text from documents
    """
    
    def __init__(self, method: str = None):
        """
        Initialize Text Extractor
        
        Args:
            method: Extraction method ('pypdf', 'pdfplumber', 'hybrid')
                   Defaults to config setting
        """
        self.method = method or EXTRACTION_CONFIG.get("extraction_method", "hybrid")
        logger.info(f"TextExtractor initialized with method: {self.method}")
    
    def extract(self, file_path: str) -> ExtractionResult:
        """
        Extract text from a document
        
        STANDARDIZED OUTPUT: Returns ExtractionResult dataclass
        
        Args:
            file_path: Path to document file
            
        Returns:
            ExtractionResult object containing:
                - raw_text: Extracted text
                - num_pages: Number of pages
                - extraction_method: Method used
                - extraction_time_seconds: Processing time
                - metadata: Additional info
        """
        logger.info(f"Starting text extraction for: {file_path}")
        
        extractor = TextExtractorFactory.create_extractor(file_path, self.method)
        result = extractor.extract(file_path)
        
        logger.info(f"Text extraction completed: {result.file_name}")
        return result

# Convenience function for direct use
def extract_text(file_path: str, method: str = None) -> ExtractionResult:
    """
    Convenience function for text extraction
    
    Usage:
        from text_extraction import extract_text
        result = extract_text("document.pdf")
        print(result.raw_text)
    
    Args:
        file_path: Path to document
        method: Optional extraction method
        
    Returns:
        ExtractionResult
    """
    extractor = TextExtractor(method=method)
    return extractor.extract(file_path)
