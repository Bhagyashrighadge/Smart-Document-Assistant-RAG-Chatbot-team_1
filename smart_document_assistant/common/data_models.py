"""
Data Models for Smart Document Assistant
Standardized data structures for integration between modules
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class ExtractionResult:
    """
    Standard result format for text extraction
    Used as output from text_extraction module
    Used as input for text_preprocessing module
    """
    file_path: str
    file_name: str
    raw_text: str
    num_pages: int
    extraction_method: str
    extraction_time_seconds: float
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, any] = field(default_factory=dict)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "file_path": self.file_path,
            "file_name": self.file_name,
            "raw_text": self.raw_text,
            "num_pages": self.num_pages,
            "extraction_method": self.extraction_method,
            "extraction_time_seconds": self.extraction_time_seconds,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

@dataclass
class PreprocessedResult:
    """
    Standard result format for text preprocessing
    Used as output from text_preprocessing module
    Used as input for retrieval/RAG module
    """
    original_text: str
    cleaned_text: str
    text_length: int
    sentences: List[str] = field(default_factory=list)
    tokens: List[str] = field(default_factory=list)
    language: str = "en"
    cleaning_time_seconds: float = 0.0
    preprocessing_time_seconds: float = 0.0
    processing_steps: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, any] = field(default_factory=dict)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "original_text": self.original_text,
            "cleaned_text": self.cleaned_text,
            "text_length": self.text_length,
            "sentences": self.sentences,
            "tokens": self.tokens,
            "language": self.language,
            "cleaning_time_seconds": self.cleaning_time_seconds,
            "preprocessing_time_seconds": self.preprocessing_time_seconds,
            "processing_steps": self.processing_steps,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

@dataclass
class ProcessingPipeline:
    """
    Complete processing result after extraction + preprocessing
    Final output ready for RAG/Retrieval module
    """
    extraction_result: ExtractionResult
    preprocessing_result: PreprocessedResult
    total_processing_time: float = 0.0
    status: str = "completed"  # completed, failed, partial
    error_message: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "extraction_result": self.extraction_result.to_dict(),
            "preprocessing_result": self.preprocessing_result.to_dict(),
            "total_processing_time": self.total_processing_time,
            "status": self.status,
            "error_message": self.error_message,
        }
