import os
from typing import Dict, Optional
from rag_pipeline.chunker import TextChunker
from rag_pipeline.embeddings import EmbeddingModel
from rag_pipeline.vector_store import FAISSVectorStore
from rag_pipeline.retriever import Retriever


class RAGSystem:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100, 
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 device: str = "cpu", index_path: str = "faiss_index", retrieval_k: int = 5):
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.index_path = index_path
        self.retrieval_k = retrieval_k
        self.is_built = False
        
        self.chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embedding_model = EmbeddingModel(model_name=embedding_model, device=device)
        self.vector_store = FAISSVectorStore(index_path=index_path)
        self.retriever = Retriever(vector_store=self.vector_store, embedding_model=self.embedding_model, k=retrieval_k)
    
    def build_from_text(self, text: str) -> Dict:
        if not text or not isinstance(text, str) or not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            chunks = self.chunker.chunk_text(text)
            if not chunks:
                raise ValueError("No chunks generated")
            
            embeddings = self.embedding_model.encode_batch(chunks)
            self.vector_store.create_index(embeddings, chunks)
            self.is_built = True
            
            return {
                "status": "success",
                "chunk_count": len(chunks),
                "embedding_dimension": self.embedding_model.get_embeddings_dimension(),
                "text_length": len(text)
            }
        except Exception as e:
            self.is_built = False
            raise RuntimeError(f"Build failed: {str(e)}")
    
    def load_existing(self) -> bool:
        try:
            success = self.vector_store.load_index()
            if success:
                self.is_built = True
            return success
        except Exception:
            return False
    
    def query(self, question: str, k: Optional[int] = None) -> Dict:
        if not self.is_built:
            raise RuntimeError("RAG system not built. Call build_from_text() first.")
        
        if not question or not isinstance(question, str) or not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            search_k = k if k is not None else self.retrieval_k
            results = self.retriever.retrieve(question, k=search_k)
            context = self.retriever.build_context(question, k=search_k)
            
            return {
                "status": "success",
                "question": question,
                "context": context,
                "source_documents": results,
                "retrieval_count": len(results)
            }
        except Exception as e:
            return {
                "status": "error",
                "question": question,
                "context": "",
                "source_documents": [],
                "retrieval_count": 0,
                "error": str(e)
            }
    
    def reset(self) -> None:
        try:
            for file in os.listdir(self.index_path):
                file_path = os.path.join(self.index_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            self.is_built = False
        except Exception as e:
            raise RuntimeError(f"Reset failed: {str(e)}")
    
    def get_vector_count(self) -> int:
        return self.vector_store.get_vector_count()
