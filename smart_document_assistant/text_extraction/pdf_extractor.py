"""
PDF Text Extraction Module
Handles PDF parsing using PyPDF2 and pdfplumber
Returns standardized ExtractionResult
"""

import time
from pathlib import Path
from typing import Tuple, Optional
import PyPDF2
import pdfplumber

from common.logger import setup_logger
from common.exceptions import (
    ExtractionError, InvalidPDFError, UnsupportedFormatError
)
from common.data_models import ExtractionResult
from config.settings import EXTRACTION_CONFIG

logger = setup_logger(__name__)

class PDFExtractor:
    """Extract text from PDF files using multiple methods"""
    
    def __init__(self, method: str = "hybrid"):
        """
        Initialize PDF Extractor
        
        Args:
            method: 'pypdf', 'pdfplumber', or 'hybrid'
        """
        self.method = method
        logger.info(f"PDFExtractor initialized with method: {method}")
    
    def extract_with_pypdf(self, pdf_path: str) -> Tuple[str, int]:
        """
        Extract text using PyPDF2
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, num_pages)
        """
        try:
            text = ""
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                    except Exception as page_error:
                        logger.warning(f"Error extracting page {page_num + 1}: {str(page_error)}")
                        continue
            
            if not text.strip():
                raise InvalidPDFError("No text extracted from PDF (possible scanned image)")
            
            logger.info(f"Successfully extracted text using PyPDF2 from {num_pages} pages")
            return text, num_pages
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {str(e)}")
            raise ExtractionError(f"PyPDF2 extraction failed: {str(e)}")
    
    def extract_with_pdfplumber(self, pdf_path: str) -> Tuple[str, int]:
        """
        Extract text using pdfplumber (better for structured content)
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, num_pages)
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                    except Exception as page_error:
                        logger.warning(f"Error extracting page {page_num + 1} with pdfplumber: {str(page_error)}")
                        continue
            
            if not text.strip():
                raise InvalidPDFError("No text extracted from PDF")
            
            logger.info(f"Successfully extracted text using pdfplumber from {num_pages} pages")
            return text, num_pages
            
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {str(e)}")
            raise ExtractionError(f"pdfplumber extraction failed: {str(e)}")
    
    def extract_with_hybrid(self, pdf_path: str) -> Tuple[str, int]:
        """
        Try pdfplumber first (better quality), fallback to PyPDF2
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, num_pages)
        """
        try:
            logger.info("Attempting hybrid extraction: pdfplumber first")
            return self.extract_with_pdfplumber(pdf_path)
        except Exception as pdfplumber_error:
            logger.warning(f"pdfplumber failed, falling back to PyPDF2: {str(pdfplumber_error)}")
            try:
                return self.extract_with_pypdf(pdf_path)
            except Exception as pypdf_error:
                logger.error(f"Both extraction methods failed")
                raise ExtractionError(
                    f"Hybrid extraction failed. pdfplumber: {str(pdfplumber_error)}, "
                    f"PyPDF2: {str(pypdf_error)}"
                )
    
    def extract(self, pdf_path: str) -> ExtractionResult:
        """
        Main extraction method - returns standardized ExtractionResult
        
        INTEGRATION POINT: Returns ExtractionResult dataclass
        This is the standard format consumed by text_preprocessing module
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            ExtractionResult object
        """
        try:
            # Validate file
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            if pdf_path.suffix.lower() != ".pdf":
                raise UnsupportedFormatError(f"Only PDF files are supported, got: {pdf_path.suffix}")
            
            file_size_mb = pdf_path.stat().st_size / (1024 * 1024)
            if file_size_mb > EXTRACTION_CONFIG["max_file_size_mb"]:
                raise ExtractionError(
                    f"File size {file_size_mb:.2f}MB exceeds limit of {EXTRACTION_CONFIG['max_file_size_mb']}MB"
                )
            
            # Extract based on method
            start_time = time.time()
            
            if self.method == "pypdf":
                raw_text, num_pages = self.extract_with_pypdf(str(pdf_path))
            elif self.method == "pdfplumber":
                raw_text, num_pages = self.extract_with_pdfplumber(str(pdf_path))
            else:  # hybrid
                raw_text, num_pages = self.extract_with_hybrid(str(pdf_path))
            
            extraction_time = time.time() - start_time
            
            # Create standardized result
            result = ExtractionResult(
                file_path=str(pdf_path),
                file_name=pdf_path.name,
                raw_text=raw_text,
                num_pages=num_pages,
                extraction_method=self.method,
                extraction_time_seconds=extraction_time,
                metadata={
                    "file_size_mb": file_size_mb,
                    "encoding": "utf-8",
                }
            )
            
            logger.info(f"Extraction completed successfully in {extraction_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            raise

class TextExtractorFactory:
    """Factory for creating appropriate text extractors"""
    
    @staticmethod
    def create_extractor(file_path: str, method: str = "hybrid") -> PDFExtractor:
        """
        Create appropriate extractor based on file type
        
        Args:
            file_path: Path to file
            method: Extraction method
            
        Returns:
            Extractor instance
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == ".pdf":
            return PDFExtractor(method=method)
        else:
            raise UnsupportedFormatError(f"Unsupported file format: {file_ext}")
