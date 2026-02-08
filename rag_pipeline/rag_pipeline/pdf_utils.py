import PyPDF2
from typing import List


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        if not text.strip():
            raise ValueError("No text found in PDF")
        
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes"""
    try:
        import io
        file = io.BytesIO(pdf_bytes)
        reader = PyPDF2.PdfReader(file)
        
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        if not text.strip():
            raise ValueError("No text found in PDF")
        
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text: {str(e)}")
