"""
Utility functions for API
"""
import os
import tempfile
from fastapi import UploadFile
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def save_upload_file(upload_file: UploadFile) -> Optional[str]:
    """
    Save uploaded file to temporary directory
    
    Args:
        upload_file: Uploaded file
        
    Returns:
        Path to saved file or None if save fails
    """
    try:
        # Create temporary file
        suffix = os.path.splitext(upload_file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await upload_file.read()
            temp_file.write(content)
            return temp_file.name
    except Exception as e:
        logger.error(f"Error saving upload file: {str(e)}")
        return None


def cleanup_temp_file(file_path: str) -> bool:
    """
    Delete temporary file
    
    Args:
        file_path: Path to file
        
    Returns:
        True if deletion successful
    """
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting temp file: {str(e)}")
        return False


def validate_pdf_file(upload_file: UploadFile) -> bool:
    """
    Validate that uploaded file is a PDF
    
    Args:
        upload_file: Uploaded file
        
    Returns:
        True if file is valid PDF
    """
    # Check file extension
    if not upload_file.filename.lower().endswith('.pdf'):
        return False
    
    # Check MIME type (if available)
    if upload_file.content_type and upload_file.content_type != "application/pdf":
        return False
    
    return True
