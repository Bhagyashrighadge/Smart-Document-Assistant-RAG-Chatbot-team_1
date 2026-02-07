from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class Embeddings:
    """Wrapper around HuggingFace sentence-transformers embeddings.

    Provides `encode` compatible with FAISS (numpy arrays).
    """

    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)

    def encode(self, texts: List[str]) -> List[np.ndarray]:
        """Encode a list of texts into embeddings (numpy arrays).

        Returns a list of 1D numpy arrays.
        """
        embs = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        # Ensure shape: (n, dim) -> list of arrays
        return [emb for emb in embs]

    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
