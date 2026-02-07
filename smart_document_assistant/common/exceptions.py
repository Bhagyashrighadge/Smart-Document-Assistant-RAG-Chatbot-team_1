"""
Custom Exceptions for Smart Document Assistant
Unified error handling across all modules
"""

class DocumentProcessingError(Exception):
    """Base exception for all document processing errors"""
    pass

class ExtractionError(DocumentProcessingError):
    """Raised when PDF text extraction fails"""
    pass

class PreprocessingError(DocumentProcessingError):
    """Raised when text preprocessing fails"""
    pass

class UnsupportedFormatError(DocumentProcessingError):
    """Raised when file format is not supported"""
    pass

class FileSizeError(DocumentProcessingError):
    """Raised when file size exceeds limit"""
    pass

class InvalidPDFError(DocumentProcessingError):
    """Raised when PDF is corrupted or invalid"""
    pass

class LanguageNotSupportedError(DocumentProcessingError):
    """Raised when language is not supported"""
    pass

class TimoutError(DocumentProcessingError):
    """Raised when processing exceeds timeout"""
    pass
