import os
import numpy as np
import pickle
from typing import List, Tuple, Optional
import faiss


class FAISSVectorStore:
    
    def __init__(self, index_path: str = "faiss_index"):
        self.index_path = index_path
        self.index = None
        self.metadata = None
        self.embedding_dimension = None
        
        if not os.path.exists(index_path):
            os.makedirs(index_path, exist_ok=True)
    
    def create_index(self, embeddings: np.ndarray, texts: List[str]) -> None:
        if not isinstance(embeddings, np.ndarray) or not isinstance(texts, list):
            raise ValueError("Invalid input types")
        
        if len(embeddings) != len(texts) or len(embeddings) == 0:
            raise ValueError("Embeddings and texts must have same non-zero length")
        
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(np.float32)
        
        try:
            self.embedding_dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(self.embedding_dimension)
            self.index.add(embeddings)
            self.metadata = texts
            self.save_index()
        except Exception as e:
            raise RuntimeError(f"Failed to create index: {str(e)}")
    
    def save_index(self) -> None:
        if self.index is None or self.metadata is None:
            raise RuntimeError("No index to save")
        
        try:
            index_file = os.path.join(self.index_path, "faiss.index")
            metadata_file = os.path.join(self.index_path, "metadata.pkl")
            
            faiss.write_index(self.index, index_file)
            with open(metadata_file, 'wb') as f:
                pickle.dump(self.metadata, f)
        except Exception as e:
            raise RuntimeError(f"Failed to save index: {str(e)}")
    
    def load_index(self) -> bool:
        try:
            index_file = os.path.join(self.index_path, "faiss.index")
            metadata_file = os.path.join(self.index_path, "metadata.pkl")
            
            if not os.path.exists(index_file):
                return False
            
            self.index = faiss.read_index(index_file)
            
            if os.path.exists(metadata_file):
                with open(metadata_file, 'rb') as f:
                    self.metadata = pickle.load(f)
            
            if self.index:
                self.embedding_dimension = self.index.d
            
            return True
        except Exception:
            return False
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> Tuple[List[float], List[str]]:
        if self.index is None:
            raise RuntimeError("Index not loaded")
        
        if k <= 0 or k > self.index.ntotal:
            k = min(k, self.index.ntotal)
        
        try:
            if query_embedding.dtype != np.float32:
                query_embedding = query_embedding.astype(np.float32)
            
            if query_embedding.ndim == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            distances, indices = self.index.search(query_embedding, k)
            distances = distances[0].tolist()
            
            results = []
            for idx in indices[0]:
                if idx >= 0 and idx < len(self.metadata):
                    results.append(self.metadata[idx])
            
            return distances, results
        except Exception as e:
            raise RuntimeError(f"Search failed: {str(e)}")
    
    def get_vector_count(self) -> int:
        return self.index.ntotal if self.index else 0
