"""
Processing Pipeline - Complete Integration
Combines text extraction and preprocessing into single pipeline
Easy integration point for other modules
"""

import time
from typing import Union, Optional

from text_extraction import extract_text
from text_preprocessing import preprocess_text
from common.logger import setup_logger
from common.data_models import ExtractionResult, PreprocessedResult, ProcessingPipeline
from common.exceptions import DocumentProcessingError

logger = setup_logger(__name__)

class DocumentProcessingPipeline:
    """
    Complete document processing pipeline
    
    INTEGRATION POINT: Main entry point for other modules
    
    Usage:
        from smart_document_assistant.pipeline import DocumentProcessingPipeline
        
        pipeline = DocumentProcessingPipeline()
        result = pipeline.process("document.pdf", language="en")
        
        # Access results
        print(result.extraction_result.raw_text)
        print(result.preprocessing_result.cleaned_text)
        print(result.preprocessing_result.sentences)
    """
    
    def __init__(self):
        """Initialize processing pipeline"""
        logger.info("DocumentProcessingPipeline initialized")
    
    def process(
        self,
        file_path: str,
        language: str = "en",
        extraction_method: str = "hybrid"
    ) -> ProcessingPipeline:
        """
        Complete document processing: Extraction + Preprocessing
        
        STANDARDIZED OUTPUT: Returns ProcessingPipeline with both results
        
        Args:
            file_path: Path to PDF document
            language: Target language ('en', 'hi', 'mr')
            extraction_method: PDF extraction method
            
        Returns:
            ProcessingPipeline object containing:
                - extraction_result: ExtractionResult
                - preprocessing_result: PreprocessedResult
                - total_processing_time: Total time taken
                - status: 'completed', 'failed', or 'partial'
        """
        try:
            start_time = time.time()
            logger.info(f"Starting document processing pipeline for: {file_path}")
            
            # Step 1: Extract text
            try:
                logger.info("Step 1: Extracting text...")
                extraction_result = extract_text(file_path, method=extraction_method)
                logger.info(f"✓ Extraction completed in {extraction_result.extraction_time_seconds:.2f}s")
            except Exception as e:
                logger.error(f"Extraction failed: {str(e)}")
                raise DocumentProcessingError(f"Extraction phase failed: {str(e)}")
            
            # Step 2: Preprocess text
            try:
                logger.info("Step 2: Preprocessing text...")
                preprocessing_result = preprocess_text(extraction_result, language=language)
                logger.info(
                    f"✓ Preprocessing completed in "
                    f"{preprocessing_result.cleaning_time_seconds + preprocessing_result.preprocessing_time_seconds:.2f}s"
                )
            except Exception as e:
                logger.error(f"Preprocessing failed: {str(e)}")
                # Create partial result if preprocessing fails
                preprocessing_result = PreprocessedResult(
                    original_text=extraction_result.raw_text,
                    cleaned_text="",
                    text_length=0,
                    language=language,
                    metadata={"error": str(e)}
                )
                status = "partial"
            else:
                status = "completed"
            
            total_time = time.time() - start_time
            
            # Create final result
            result = ProcessingPipeline(
                extraction_result=extraction_result,
                preprocessing_result=preprocessing_result,
                total_processing_time=total_time,
                status=status
            )
            
            logger.info(f"✓ Document processing completed in {total_time:.2f}s - Status: {status}")
            return result
            
        except Exception as e:
            logger.error(f"Document processing pipeline failed: {str(e)}")
            raise

# Convenience function
def process_document(
    file_path: str,
    language: str = "en",
    extraction_method: str = "hybrid"
) -> ProcessingPipeline:
    """
    Convenience function for complete document processing
    
    Usage:
        from smart_document_assistant import process_document
        
        result = process_document("document.pdf", language="en")
        print(result.preprocessing_result.sentences)
    
    Args:
        file_path: Path to PDF document
        language: Target language
        extraction_method: PDF extraction method
        
    Returns:
        ProcessingPipeline
    """
    pipeline = DocumentProcessingPipeline()
    return pipeline.process(file_path, language, extraction_method)
