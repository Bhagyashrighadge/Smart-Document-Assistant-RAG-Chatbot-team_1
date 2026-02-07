from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    
    DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    def __init__(self, model_name: str = DEFAULT_MODEL, device: str = "cpu"):
        if not model_name:
            raise ValueError("model_name cannot be empty")
        
        self.model_name = model_name
        self.device = device
        
        try:
            self.model = SentenceTransformer(model_name, device=device)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    def encode_single(self, text: str) -> np.ndarray:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string")
        
        try:
            return self.model.encode(text, convert_to_numpy=True)
        except Exception as e:
            raise RuntimeError(f"Failed to encode text: {str(e)}")
    
    def encode_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        if not isinstance(texts, list) or not texts:
            raise ValueError("Texts must be a non-empty list")
        
        valid_texts = [t for t in texts if isinstance(t, str) and t.strip()]
        if not valid_texts:
            raise ValueError("No valid texts to encode")
        
        try:
            embeddings = self.model.encode(
                valid_texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            return embeddings
        except Exception as e:
            raise RuntimeError(f"Failed to encode batch: {str(e)}")
    
    def get_query_embedding(self, query: str) -> np.ndarray:
        return self.encode_single(query)
    
    def get_embeddings_dimension(self) -> int:
        return self.embedding_dim
