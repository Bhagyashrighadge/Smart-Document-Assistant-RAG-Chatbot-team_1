from typing import List, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        if chunk_size <= 0 or chunk_overlap < 0:
            raise ValueError("Invalid chunk parameters")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
            length_function=len,
            is_separator_regex=False
        )
    
    def chunk_text(self, text: str) -> List[str]:
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        
        if not text.strip():
            return []
        
        try:
            chunks = self.splitter.split_text(text)
            chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
            return chunks
        except Exception as e:
            raise RuntimeError(f"Chunking failed: {str(e)}")
    
    def get_chunks_with_info(self, text: str) -> List[dict]:
        chunks = self.chunk_text(text)
        return [
            {
                "chunk_id": idx,
                "text": chunk,
                "length": len(chunk)
            }
            for idx, chunk in enumerate(chunks)
        ]
