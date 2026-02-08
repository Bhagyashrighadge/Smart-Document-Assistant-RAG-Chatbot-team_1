"""
Test Suite for Document Processing Modules
Unit and integration tests
"""

import pytest
from pathlib import Path
import tempfile

from text_extraction import extract_text
from text_preprocessing import preprocess_text
from pipeline import process_document
from common.data_models import ExtractionResult, PreprocessedResult

# ==================== FIXTURES ====================

@pytest.fixture
def sample_pdf_path():
    """Provide path to a test PDF (create if needed)"""
    # This assumes you have a test PDF in tests/fixtures/
    pdf_path = Path(__file__).parent / "fixtures" / "sample.pdf"
    return str(pdf_path)

@pytest.fixture
def sample_text():
    """Provide sample text for testing"""
    return """
    This is a sample text for testing.
    It contains multiple sentences.
    The text also has URLs like https://example.com and emails test@example.com.
    Additional content here with numbers like 123 and 456.
    """

# ==================== TEXT EXTRACTION TESTS ====================

class TestTextExtraction:
    """Tests for text extraction module"""
    
    def test_extract_text_returns_extraction_result(self, sample_pdf_path):
        """Test that extract_text returns ExtractionResult"""
        result = extract_text(sample_pdf_path)
        assert isinstance(result, ExtractionResult)
        assert result.raw_text
        assert result.num_pages > 0
        assert result.extraction_time_seconds > 0
    
    def test_extraction_result_has_metadata(self, sample_pdf_path):
        """Test that result contains required metadata"""
        result = extract_text(sample_pdf_path)
        assert result.file_name
        assert result.file_path
        assert result.extraction_method in ["pypdf", "pdfplumber", "hybrid"]
        assert result.metadata
    
    def test_extract_with_different_methods(self, sample_pdf_path):
        """Test extraction with different methods"""
        for method in ["pypdf", "pdfplumber", "hybrid"]:
            result = extract_text(sample_pdf_path, method=method)
            assert isinstance(result, ExtractionResult)
            assert result.extraction_method == method

# ==================== TEXT PREPROCESSING TESTS ====================

class TestTextPreprocessing:
    """Tests for text preprocessing module"""
    
    def test_preprocess_text_returns_preprocessed_result(self, sample_text):
        """Test that preprocess_text returns PreprocessedResult"""
        result = preprocess_text(sample_text)
        assert isinstance(result, PreprocessedResult)
        assert result.cleaned_text
        assert len(result.sentences) > 0
        assert len(result.tokens) > 0
    
    def test_preprocessing_cleans_text(self, sample_text):
        """Test that URLs and emails are removed"""
        result = preprocess_text(sample_text)
        assert "https://" not in result.cleaned_text
        assert "example.com" not in result.cleaned_text
        assert "test@" not in result.cleaned_text
    
    def test_preprocessing_supports_multiple_languages(self, sample_text):
        """Test preprocessing for different languages"""
        for lang in ["en", "hi", "mr"]:
            result = preprocess_text(sample_text, language=lang)
            assert result.language == lang
    
    def test_preprocessing_result_has_metadata(self, sample_text):
        """Test that result contains required metadata"""
        result = preprocess_text(sample_text)
        assert result.cleaning_time_seconds > 0
        assert result.preprocessing_time_seconds >= 0
        assert len(result.processing_steps) > 0
        assert result.metadata

# ==================== PIPELINE TESTS ====================

class TestDocumentProcessingPipeline:
    """Tests for complete processing pipeline"""
    
    def test_pipeline_returns_processing_pipeline(self, sample_pdf_path):
        """Test that pipeline returns complete result"""
        result = process_document(sample_pdf_path)
        assert result.extraction_result
        assert result.preprocessing_result
        assert result.total_processing_time > 0
        assert result.status in ["completed", "partial", "failed"]
    
    def test_pipeline_extracts_and_preprocesses(self, sample_pdf_path):
        """Test that pipeline performs both steps"""
        result = process_document(sample_pdf_path)
        assert result.extraction_result.raw_text
        assert result.preprocessing_result.cleaned_text
        assert result.preprocessing_result.sentences
    
    def test_pipeline_with_different_languages(self, sample_pdf_path):
        """Test pipeline with different languages"""
        for lang in ["en", "hi", "mr"]:
            result = process_document(sample_pdf_path, language=lang)
            assert result.preprocessing_result.language == lang

# ==================== INTEGRATION TESTS ====================

class TestIntegration:
    """Integration tests between modules"""
    
    def test_extraction_result_works_with_preprocessing(self, sample_pdf_path):
        """Test that ExtractionResult can be consumed by preprocessing"""
        extraction = extract_text(sample_pdf_path)
        preprocessing = preprocess_text(extraction)
        assert preprocessing.cleaned_text
    
    def test_full_pipeline_consistency(self, sample_pdf_path):
        """Test that pipeline produces consistent results"""
        # Run pipeline
        pipeline_result = process_document(sample_pdf_path)
        
        # Run modules separately
        extraction = extract_text(sample_pdf_path)
        preprocessing = preprocess_text(extraction)
        
        # Compare results
        assert pipeline_result.extraction_result.raw_text == extraction.raw_text
        assert pipeline_result.preprocessing_result.cleaned_text == preprocessing.cleaned_text

# ==================== PERFORMANCE TESTS ====================

class TestPerformance:
    """Performance and timing tests"""
    
    def test_extraction_completes_within_timeout(self, sample_pdf_path):
        """Test that extraction completes within expected time"""
        result = extract_text(sample_pdf_path)
        assert result.extraction_time_seconds < 300  # 5 minutes max
    
    def test_preprocessing_completes_quickly(self, sample_text):
        """Test that preprocessing is fast"""
        result = preprocess_text(sample_text)
        total_time = result.cleaning_time_seconds + result.preprocessing_time_seconds
        assert total_time < 10  # Should be much faster

# ==================== ERROR HANDLING TESTS ====================

class TestErrorHandling:
    """Error handling and edge cases"""
    
    def test_extract_nonexistent_file(self):
        """Test extraction with non-existent file"""
        with pytest.raises(FileNotFoundError):
            extract_text("/nonexistent/path/file.pdf")
    
    def test_extract_unsupported_format(self):
        """Test extraction with unsupported format"""
        with pytest.raises(Exception):  # Should raise UnsupportedFormatError
            extract_text("file.txt")
    
    def test_preprocess_empty_text(self):
        """Test preprocessing empty text"""
        result = preprocess_text("")
        assert result.cleaned_text == ""
        assert len(result.sentences) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
