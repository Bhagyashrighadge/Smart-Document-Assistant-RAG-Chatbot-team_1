"""
Embedding Service - Generate embeddings using Sentence Transformers
"""
from typing import List
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Handles text embedding generation"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding service
        
        Args:
            model_name: Name of the Sentence Transformer model to use
        """
        try:
            # Lazy import to avoid tensorflow issues
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            logger.info(f"[EMBEDDING] Embedding text: {len(text)} chars")
            embedding = self.model.encode(text)
            result = embedding.tolist()
            logger.info(f"[EMBEDDING] ✓ Embedding generated: {len(result)} dimensions")
            return result
        except Exception as e:
            logger.error(f"[EMBEDDING] Error generating embedding: {str(e)}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            logger.info(f"[EMBEDDING] Embedding {len(texts)} texts")
            total_chars = sum(len(t) for t in texts)
            logger.info(f"[EMBEDDING] Total characters: {total_chars}")
            
            embeddings = self.model.encode(texts)
            result = [emb.tolist() for emb in embeddings]
            
            logger.info(f"[EMBEDDING] ✓ Generated {len(result)} embeddings of {len(result[0]) if result else 0} dimensions each")
            return result
        except Exception as e:
            logger.error(f"[EMBEDDING] Error generating embeddings: {str(e)}")
            raise
