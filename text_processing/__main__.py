"""
__main__.py - Quick test script for the module
Run this to verify everything is working: python -m text_processing
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all imports work"""
    print("Testing imports...")
    try:
        from text_processing import (
            process_document,
            extract_text,
            preprocess_text,
            ExtractionResult,
            PreprocessedResult,
            ProcessingPipeline
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_configuration():
    """Test if configuration loads"""
    print("\\nTesting configuration...")
    try:
        from config.settings import (
            EXTRACTION_CONFIG,
            PREPROCESSING_CONFIG,
            NLP_CONFIG,
            LOGGING_CONFIG
        )
        print(f"✓ Configuration loaded")
        print(f"  - Extraction method: {EXTRACTION_CONFIG['extraction_method']}")
        print(f"  - Max file size: {EXTRACTION_CONFIG['max_file_size_mb']} MB")
        print(f"  - Log level: {LOGGING_CONFIG['level']}")
        return True
    except Exception as e:
        print(f"✗ Configuration load failed: {e}")
        return False

def test_logger():
    """Test if logger works"""
    print("\\nTesting logger...")
    try:
        from common.logger import setup_logger
        logger = setup_logger("test")
        logger.info("Logger test message")
        print("✓ Logger working")
        return True
    except Exception as e:
        print(f"✗ Logger failed: {e}")
        return False

def show_info():
    """Show project information"""
    print("\\n" + "="*60)
    print("Smart Document Assistant - Document Processing Module")
    print("="*60)
    print("\\nVersion: 1.0.0")
    print("Person: Person 3 - Document Processing Engineer")
    print("\\nModules:")
    print("  1. Text Extraction (PDF parsing)")
    print("  2. Text Preprocessing (Cleaning & NLP)")
    print("  3. Pipeline (Combined processing)")
    print("\\nCapabilities:")
    print("  • Extract text from PDF files")
    print("  • Clean and preprocess text")
    print("  • Support for English, Hindi, Marathi")
    print("  • REST API for microservices")
    print("  • Comprehensive test suite")
    print("\\nQuick Start:")
    print("  from text_processing import process_document")
    print("  result = process_document('document.pdf', language='en')")
    print("\\nDocumentation:")
    print("  • README.md - Full documentation")
    print("  • API.md - REST API documentation")
    print("  • INTEGRATION.md - Integration guide")
    print("  • COPILOT_PROMPT.md - Complete specifications")
    print("  • QUICKSTART.md - Quick start guide")
    print("\\nStart API Server:")
    print("  python -m uvicorn api:app --reload --port 8000")
    print("\\nRun Tests:")
    print("  pytest tests/test_modules.py -v")
    print("="*60 + "\\n")

if __name__ == "__main__":
    print("Smart Document Assistant - Initialization Check\\n")
    
    all_passed = True
    all_passed &= test_imports()
    all_passed &= test_configuration()
    all_passed &= test_logger()
    
    if all_passed:
        print("\\n✓ All checks passed! System is ready to use.")
        show_info()
        sys.exit(0)
    else:
        print("\\n✗ Some checks failed. Please fix the issues above.")
        sys.exit(1)
