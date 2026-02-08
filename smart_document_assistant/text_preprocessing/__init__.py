"""
Text Preprocessing Module Interface
Entry point for text preprocessing with standardized API
"""

import time
from typing import Union

from text_preprocessing.cleaner import TextCleaner, TokenizerPreprocessor
from common.logger import setup_logger
from common.data_models import ExtractionResult, PreprocessedResult
from common.exceptions import PreprocessingError
from config.settings import PREPROCESSING_CONFIG, NLP_CONFIG

logger = setup_logger(__name__)

class TextPreprocessor:
    """
    Main interface for text preprocessing
    INTEGRATION POINT: Use this class to preprocess extracted text
    Consumes: ExtractionResult (from text_extraction module)
    Produces: PreprocessedResult (for retrieval/RAG module)
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize Text Preprocessor
        
        Args:
            language: Target language ('en', 'hi', 'mr')
        """
        self.language = language
        self.cleaner = TextCleaner(PREPROCESSING_CONFIG)
        self.tokenizer = TokenizerPreprocessor(language)
        logger.info(f"TextPreprocessor initialized for language: {language}")
    
    def preprocess(
        self, 
        extraction_result: Union[ExtractionResult, str],
        language: str = None
    ) -> PreprocessedResult:
        """
        Preprocess extracted text
        
        STANDARDIZED INPUT: Accepts ExtractionResult from text_extraction module
        STANDARDIZED OUTPUT: Returns PreprocessedResult dataclass
        
        Args:
            extraction_result: Either ExtractionResult object or raw text string
            language: Override default language
            
        Returns:
            PreprocessedResult object containing:
                - cleaned_text: Preprocessed text
                - sentences: List of sentences
                - tokens: List of tokens
                - processing_steps: Steps applied
                - cleaning_time_seconds: Time for cleaning
                - preprocessing_time_seconds: Time for NLP preprocessing
        """
        try:
            start_time = time.time()
            
            # Handle both ExtractionResult and raw text
            if isinstance(extraction_result, ExtractionResult):
                original_text = extraction_result.raw_text
                file_name = extraction_result.file_name
            else:
                original_text = extraction_result
                file_name = "raw_text"
            
            logger.info(f"Starting text preprocessing for: {file_name}")
            
            # Update language if provided
            if language:
                self.language = language
                self.tokenizer = TokenizerPreprocessor(language)
            
            # Step 1: Clean text
            cleaned_text, cleaning_steps, cleaning_time = self.cleaner.clean(original_text)
            
            # Step 2: NLP preprocessing (tokenization, etc.)
            sentences, tokens, preprocessing_time = self.tokenizer.preprocess(cleaned_text)
            
            total_time = time.time() - start_time
            
            # Create standardized result
            result = PreprocessedResult(
                original_text=original_text,
                cleaned_text=cleaned_text,
                text_length=len(cleaned_text),
                sentences=sentences,
                tokens=tokens,
                language=self.language,
                cleaning_time_seconds=cleaning_time,
                preprocessing_time_seconds=preprocessing_time,
                processing_steps=cleaning_steps,
                metadata={
                    "original_length": len(original_text),
                    "cleaned_length": len(cleaned_text),
                    "num_sentences": len(sentences),
                    "num_tokens": len(tokens),
                }
            )
            
            logger.info(f"Preprocessing completed successfully in {total_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Preprocessing failed: {str(e)}")
            raise PreprocessingError(f"Text preprocessing failed: {str(e)}")

# Convenience function for direct use
def preprocess_text(
    text: Union[ExtractionResult, str],
    language: str = "en"
) -> PreprocessedResult:
    """
    Convenience function for text preprocessing
    
    Usage:
        from text_preprocessing import preprocess_text
        from text_extraction import extract_text
        
        # Option 1: With ExtractionResult
        extraction_result = extract_text("document.pdf")
        preprocessed = preprocess_text(extraction_result, language="en")
        
        # Option 2: With raw text
        preprocessed = preprocess_text("raw text here", language="en")
    
    Args:
        text: ExtractionResult or raw text string
        language: Target language
        
    Returns:
        PreprocessedResult
    """
    preprocessor = TextPreprocessor(language=language)
    return preprocessor.preprocess(text, language=language)
