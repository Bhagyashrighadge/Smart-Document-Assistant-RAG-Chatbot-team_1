from typing import List
import re
from app.modules.embeddings import Embeddings

class QueryProcessor:
    """Cleans user queries and returns embeddings.

    Responsibilities:
    - Normalize/clean input text
    - Call embeddings module to create vectors
    """

    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings

    def clean_text(self, text: str) -> str:
        """Simple cleaning pipeline: strip, lower, normalize whitespace."""
        if not isinstance(text, str):
            raise TypeError('question must be a string')
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def vectorize(self, text: str):
        """Clean and vectorize the query using embeddings module."""
        cleaned = self.clean_text(text)
        return self.embeddings.encode([cleaned])[0]
