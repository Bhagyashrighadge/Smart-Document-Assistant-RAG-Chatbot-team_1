"""
Smart Document Assistant - RAG Pipeline Module
Modular RAG pipeline for document question-answering system
"""

from rag_pipeline.rag_system import RAGSystem
from rag_pipeline.chunker import TextChunker
from rag_pipeline.embeddings import EmbeddingModel
from rag_pipeline.vector_store import FAISSVectorStore
from rag_pipeline.retriever import Retriever

__version__ = "1.0.0"
__author__ = "RAG Pipeline Engineer"

__all__ = [
    "RAGSystem",
    "TextChunker",
    "EmbeddingModel",
    "FAISSVectorStore",
    "Retriever"
]
