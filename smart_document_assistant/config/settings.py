"""
Configuration Settings for Smart Document Assistant
Central configuration file for all module settings
"""

import os
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for dir_path in [UPLOADS_DIR, PROCESSED_DIR, LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# === TEXT EXTRACTION SETTINGS ===
EXTRACTION_CONFIG = {
    "supported_formats": ["pdf"],
    "extraction_method": "hybrid",  # Can be 'pypdf', 'pdfplumber', 'hybrid'
    "max_file_size_mb": 100,
    "timeout_seconds": 300,
}

# === TEXT PREPROCESSING SETTINGS ===
PREPROCESSING_CONFIG = {
    "remove_special_chars": True,
    "remove_extra_whitespace": True,
    "lowercase": False,  # Set to True only if needed
    "remove_urls": True,
    "remove_emails": True,
    "remove_numbers": False,
    "remove_punctuation": False,
    "min_sentence_length": 3,
    "max_sentence_length": 500,
    "language": "multilingual",  # English, Hindi, Marathi
}

# === NLP PREPROCESSING ===
NLP_CONFIG = {
    "tokenizer": "spacy",  # Options: spacy, nltk, transformers
    "remove_stopwords": True,
    "lemmatization": True,
    "pos_tagging": True,
    "supported_languages": ["en", "hi", "mr"],  # English, Hindi, Marathi
}

# === LOGGING ===
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": LOGS_DIR / "smart_document_assistant.log",
}

# === DATABASE/STORAGE ===
STORAGE_CONFIG = {
    "type": "json",  # Can be 'json', 'sqlite', 'postgresql'
    "cache_extracted_text": True,
    "cache_preprocessed_text": True,
}

# === INTEGRATION ENDPOINTS ===
# These are for other modules to call document processing functions
INTEGRATION_ENDPOINTS = {
    "extract_text": "/api/v1/extract",
    "preprocess_text": "/api/v1/preprocess",
    "process_pipeline": "/api/v1/process-full",
}
