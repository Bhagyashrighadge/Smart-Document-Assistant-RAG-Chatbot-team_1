from typing import List, Tuple, Optional, Dict
import numpy as np


class Retriever:
    
    DEFAULT_K = 5
    
    def __init__(self, vector_store, embedding_model, k: int = DEFAULT_K):
        if vector_store is None or embedding_model is None:
            raise ValueError("vector_store and embedding_model required")
        if k <= 0:
            raise ValueError("k must be greater than 0")
        
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.k = k
    
    def retrieve(self, query: str, k: Optional[int] = None) -> List[dict]:
        if not query or not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string")
        
        search_k = k if k is not None else self.k
        if search_k <= 0:
            raise ValueError("k must be greater than 0")
        
        try:
            query_embedding = self.embedding_model.get_query_embedding(query)
            distances, texts = self.vector_store.search(query_embedding, k=search_k)
            
            results = []
            for rank, (distance, text) in enumerate(zip(distances, texts), 1):
                similarity_score = 1 / (1 + distance)
                results.append({
                    'text': text,
                    'score': float(similarity_score),
                    'distance': float(distance),
                    'rank': rank
                })
            
            return results
        except Exception as e:
            raise RuntimeError(f"Retrieval failed: {str(e)}")
    
    def build_context(self, query: str, k: Optional[int] = None, separator: str = "\n\n---\n\n") -> str:
        results = self.retrieve(query, k=k)
        if not results:
            return ""
        context_parts = [result['text'] for result in results]
        return separator.join(context_parts)
    
    def set_k(self, k: int) -> None:
        if k <= 0:
            raise ValueError("k must be greater than 0")
        self.k = k
