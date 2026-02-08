"""
Text Preprocessing Module
Cleans and preprocesses extracted text
Returns standardized PreprocessedResult
"""

import re
import time
from typing import List
import string

from common.logger import setup_logger
from common.exceptions import PreprocessingError
from common.data_models import PreprocessedResult
from config.settings import PREPROCESSING_CONFIG

logger = setup_logger(__name__)

class TextCleaner:
    """Clean extracted text - remove noise and normalize"""
    
    def __init__(self, config: dict = None):
        """
        Initialize Text Cleaner
        
        Args:
            config: Preprocessing configuration
        """
        self.config = config or PREPROCESSING_CONFIG
        logger.info("TextCleaner initialized")
    
    def remove_special_characters(self, text: str) -> str:
        """Remove special characters while preserving spaces and basic punctuation"""
        if not self.config.get("remove_special_chars", True):
            return text
        
        # Keep alphanumeric, spaces, and basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\'\"\:\;\(\)\n]', '', text, flags=re.UNICODE)
        return text
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text"""
        if not self.config.get("remove_urls", True):
            return text
        
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'www\.\S+', '', text)
        return text
    
    def remove_emails(self, text: str) -> str:
        """Remove email addresses"""
        if not self.config.get("remove_emails", True):
            return text
        
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        return text
    
    def remove_numbers(self, text: str) -> str:
        """Remove numbers (optional)"""
        if not self.config.get("remove_numbers", False):
            return text
        
        text = re.sub(r'\b\d+\b', '', text)
        return text
    
    def remove_punctuation(self, text: str) -> str:
        """Remove punctuation (optional)"""
        if not self.config.get("remove_punctuation", False):
            return text
        
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text
    
    def remove_extra_whitespace(self, text: str) -> str:
        """Remove extra spaces, tabs, newlines"""
        if not self.config.get("remove_extra_whitespace", True):
            return text
        
        # Replace multiple spaces/tabs with single space
        text = re.sub(r'[ \t]+', ' ', text)
        # Replace multiple newlines with double newline
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Strip leading/trailing whitespace
        text = text.strip()
        return text
    
    def clean(self, text: str) -> tuple:
        """
        Apply all cleaning steps
        
        Args:
            text: Raw extracted text
            
        Returns:
            Tuple of (cleaned_text, processing_steps)
        """
        try:
            start_time = time.time()
            original_length = len(text)
            processing_steps = []
            
            # Apply cleaning steps in order
            text = self.remove_urls(text)
            processing_steps.append("urls_removed")
            
            text = self.remove_emails(text)
            processing_steps.append("emails_removed")
            
            text = self.remove_special_characters(text)
            processing_steps.append("special_chars_removed")
            
            text = self.remove_numbers(text)
            processing_steps.append("numbers_removed")
            
            text = self.remove_punctuation(text)
            processing_steps.append("punctuation_removed")
            
            text = self.remove_extra_whitespace(text)
            processing_steps.append("whitespace_normalized")
            
            cleaning_time = time.time() - start_time
            
            logger.info(
                f"Text cleaning completed in {cleaning_time:.2f}s. "
                f"Original length: {original_length}, Cleaned length: {len(text)}"
            )
            
            return text, processing_steps, cleaning_time
            
        except Exception as e:
            logger.error(f"Text cleaning failed: {str(e)}")
            raise PreprocessingError(f"Text cleaning failed: {str(e)}")

class TokenizerPreprocessor:
    """
    Tokenize and preprocess text using NLTK/spaCy
    Supports: sentence tokenization, word tokenization, lemmatization
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize Tokenizer
        
        Args:
            language: Language code ('en', 'hi', 'mr')
        """
        self.language = language
        
        # Try to import spacy (optional dependency)
        try:
            import spacy  # type: ignore
            try:
                if language == "en":
                    self.nlp = spacy.load("en_core_web_sm")
                elif language == "hi":
                    self.nlp = spacy.load("hi_core_web_sm")
                elif language == "mr":
                    # For Marathi, we'll use a basic tokenizer
                    self.nlp = None
                else:
                    self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning(f"spaCy model not found for {language}, using basic tokenization")
                self.nlp = None
        except ImportError:
            logger.warning("spaCy not installed, using basic tokenization")
            self.nlp = None
        
        logger.info(f"TokenizerPreprocessor initialized for language: {language}")
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        try:
            if self.nlp:
                doc = self.nlp(text)
                sentences = [sent.text.strip() for sent in doc.sents]
            else:
                # Basic sentence tokenization using regex
                sentences = re.split(r'[.!?]+', text)
                sentences = [s.strip() for s in sentences if s.strip()]
            
            # Filter by length
            min_len = self.language != "en" and 2 or 3  # Allow shorter sentences for Hindi/Marathi
            max_len = 500
            
            sentences = [
                s for s in sentences
                if min_len <= len(s.split()) <= max_len
            ]
            
            return sentences
        except Exception as e:
            logger.error(f"Sentence tokenization failed: {str(e)}")
            raise PreprocessingError(f"Sentence tokenization failed: {str(e)}")
    
    def tokenize_words(self, text: str) -> List[str]:
        """Tokenize text into words/tokens"""
        try:
            if self.nlp:
                doc = self.nlp(text)
                tokens = [token.text for token in doc]
            else:
                # Basic word tokenization
                tokens = text.split()
            
            return tokens
        except Exception as e:
            logger.error(f"Word tokenization failed: {str(e)}")
            raise PreprocessingError(f"Word tokenization failed: {str(e)}")
    
    def get_lemmas(self, text: str) -> List[str]:
        """Get lemmatized form of words (for English primarily)"""
        try:
            if not self.nlp or self.language != "en":
                # Return original tokens for non-English
                return self.tokenize_words(text)
            
            doc = self.nlp(text)
            lemmas = [token.lemma_ for token in doc]
            return lemmas
        except Exception as e:
            logger.warning(f"Lemmatization failed: {str(e)}, using original tokens")
            return self.tokenize_words(text)
    
    def preprocess(self, text: str) -> tuple:
        """
        Perform full NLP preprocessing
        
        Args:
            text: Cleaned text
            
        Returns:
            Tuple of (sentences, tokens)
        """
        try:
            start_time = time.time()
            
            sentences = self.tokenize_sentences(text)
            tokens = self.tokenize_words(text)
            
            preprocessing_time = time.time() - start_time
            
            logger.info(
                f"NLP preprocessing completed in {preprocessing_time:.2f}s. "
                f"Sentences: {len(sentences)}, Tokens: {len(tokens)}"
            )
            
            return sentences, tokens, preprocessing_time
            
        except Exception as e:
            logger.error(f"NLP preprocessing failed: {str(e)}")
            raise PreprocessingError(f"NLP preprocessing failed: {str(e)}")
