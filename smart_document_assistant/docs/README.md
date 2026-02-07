# Document Processing Module - Text Extraction & Preprocessing

## Overview

**Document Processing Module** provides PDF text extraction and preprocessing capabilities:
- Extract text from PDF files using multiple methods
- Clean and preprocess extracted text
- Tokenize text for NLP processing
- Multi-language support (English, Hindi, Marathi)

---

## Project Structure

```
smart_document_assistant/
├── __init__.py                    # Main entry point
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
│
├── config/
│   └── settings.py               # Centralized configuration
│
├── common/
│   ├── logger.py                 # Logging setup
│   ├── exceptions.py             # Custom exceptions
│   └── data_models.py            # Standardized data structures
│
├── text_extraction/
│   ├── __init__.py               # Public API for extraction
│   └── pdf_extractor.py          # PDF parsing implementation
│
├── text_preprocessing/
│   ├── __init__.py               # Public API for preprocessing
│   └── cleaner.py                # Text cleaning implementation
│
├── pipeline.py                   # Complete processing pipeline
├── api.py                        # REST API endpoints
│
├── tests/
│   └── test_modules.py           # Test suite
│
└── docs/
    ├── README.md                 # This file
    ├── API.md                    # API documentation
    └── INTEGRATION.md            # Integration guide
```

---

## Features

### Text Extraction
- **PyPDF2**: Fast PDF parsing
- **pdfplumber**: High-quality extraction
- **Hybrid mode**: Best of both (default)

### Text Preprocessing
- **Text Cleaning**: Remove URLs, emails, special characters
- **Normalization**: Fix spacing and whitespace
- **NLP Processing**: Sentence and word tokenization
- **Language Support**: English, Hindi, Marathi

### API Server
- Complete REST API with 6 endpoints
- File upload support
- JSON responses

---

## Quick Start

### Installation

```bash
# Clone or navigate to project
cd smart_document_assistant

# Install dependencies
pip install -r requirements.txt

# Download NLP models (optional, for enhanced processing)
python -m spacy download en_core_web_sm
```

### Basic Usage

```python
# Option 1: Simple usage - Extract only
from smart_document_assistant import extract_text

result = extract_text(\"document.pdf\")
print(result.raw_text)

# Option 2: Preprocess only
from smart_document_assistant import preprocess_text

preprocessed = preprocess_text(\"raw text here\", language=\"en\")
print(preprocessed.cleaned_text)

# Option 3: Complete pipeline (RECOMMENDED)
from smart_document_assistant import process_document

result = process_document(\"document.pdf\", language=\"en\")
print(result.preprocessing_result.sentences)
```

### Running API Server

```bash
# Start FastAPI server
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Test API
curl -X POST http://localhost:8000/api/v1/process-full \\
  -H \"Content-Type: application/json\" \\
  -d {\"file_path\": \"document.pdf\", \"language\": \"en\"}
```

---

## Data Models (Integration Contracts)

### ExtractionResult
Output from text extraction module:
```python
@dataclass
class ExtractionResult:
    file_path: str              # Original file path
    file_name: str              # File name only
    raw_text: str               # Extracted text
    num_pages: int              # Number of pages
    extraction_method: str      # Method used
    extraction_time_seconds: float  # Processing time
    timestamp: datetime         # When extracted
    metadata: Dict[str, any]    # Additional info
```

### PreprocessedResult
Output from text preprocessing module:
```python
@dataclass
class PreprocessedResult:
    original_text: str          # Original text before cleaning
    cleaned_text: str           # Cleaned text
    text_length: int            # Length of cleaned text
    sentences: List[str]        # Sentence tokenization
    tokens: List[str]           # Word tokenization
    language: str               # Language code
    cleaning_time_seconds: float
    preprocessing_time_seconds: float
    processing_steps: List[str] # Steps applied
    metadata: Dict[str, any]    # Statistics
```

### ProcessingPipeline
Complete result with both extraction and preprocessing:
```python
@dataclass
class ProcessingPipeline:
    extraction_result: ExtractionResult      # From step 1
    preprocessing_result: PreprocessedResult # From step 2
    total_processing_time: float             # Total time
    status: str                              # completed/failed/partial
```

---

## Configuration

Edit `config/settings.py` to customize behavior:

```python
# Text extraction settings
EXTRACTION_CONFIG = {
    \"extraction_method\": \"hybrid\",      # pypdf, pdfplumber, hybrid
    \"max_file_size_mb\": 100,
    \"timeout_seconds\": 300,
}

# Text preprocessing settings
PREPROCESSING_CONFIG = {
    \"remove_special_chars\": True,
    \"remove_urls\": True,
    \"remove_emails\": True,
    \"remove_numbers\": False,
    \"remove_punctuation\": False,
}

# NLP settings
NLP_CONFIG = {
    \"remove_stopwords\": True,
    \"lemmatization\": True,
    \"supported_languages\": [\"en\", \"hi\", \"mr\"],
}
```

---

## Error Handling

Custom exceptions for clear error messages:

```python
from smart_document_assistant.common.exceptions import (
    ExtractionError,
    PreprocessingError,
    UnsupportedFormatError,
    FileSizeError,
)

try:
    result = process_document(\"document.pdf\")
except UnsupportedFormatError as e:
    print(f\"File format not supported: {e}\")
except FileSizeError as e:
    print(f\"File too large: {e}\")
except ExtractionError as e:
    print(f\"Extraction failed: {e}\")
```

---

## Testing

Run test suite:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test
pytest tests/test_modules.py::TestTextExtraction -v
```

---

## Integration with Other Modules

### Retrieval/RAG Module
The `PreprocessedResult` is ready for your retrieval system:

```python
from smart_document_assistant import process_document

# Get preprocessed document
result = process_document(\"document.pdf\", language=\"en\")

# Pass to retrieval module
sentences = result.preprocessing_result.sentences
tokens = result.preprocessing_result.tokens
cleaned_text = result.preprocessing_result.cleaned_text

# Forward to embedding/vectorization
your_retrieval_module.index(sentences)
```

### LLM/Chat Module
Use both extraction and preprocessing results:

```python
# Full processing pipeline
result = process_document(\"document.pdf\", language=\"en\")

# Send to chat module
chat_context = {
    \"original_text\": result.extraction_result.raw_text,
    \"cleaned_text\": result.preprocessing_result.cleaned_text,
    \"sentences\": result.preprocessing_result.sentences,
    \"language\": result.preprocessing_result.language,
}

your_chat_module.initialize_context(chat_context)
```

---

## API Reference

See [API.md](API.md) for detailed API documentation.

---

## Performance Metrics

Typical processing times (on standard hardware):
- **Text Extraction**: 0.5-5 seconds per document
- **Text Preprocessing**: 0.1-1 second per document
- **Complete Pipeline**: 0.6-6 seconds per document

---

## Logging

Logs are saved to `logs/smart_document_assistant.log`:

```python
from smart_document_assistant.common.logger import setup_logger

logger = setup_logger(__name__)
logger.info(\"Processing started\")
logger.error(\"Processing failed\")
```

---

## Troubleshooting

### PDF Extraction Returns Empty String
- PDF might be image-based (scanned)
- Try hybrid method: `.extract(file_path, method=\"hybrid\")`
- Check PDF file is not corrupted

### spaCy Model Not Found
```bash
python -m spacy download en_core_web_sm
python -m spacy download hi_core_web_sm
```

### API Port Already in Use
```bash
# Use different port
python -m uvicorn api:app --port 8001
```

---

## Contributing

For team integration:
1. Keep imports minimal and explicit
2. Always return standardized data models
3. Document additional dependencies
4. Add tests for new features
5. Update this documentation

---

## Version

Current: **1.0.0**

---



---

## Next Steps

1. Follow the Quick Start guide
2. Process your first PDF document
3. Review the output
4. Customize settings as needed

---

For API documentation, see [API.md](API.md)
