"""
RAG Pipeline Service - Complete RAG pipeline implementation
"""
import chromadb
from chromadb.config import Settings
from typing import List, Tuple, Optional
import logging
from .embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Complete RAG pipeline with ChromaDB"""
    
    def __init__(self):
        """Initialize RAG pipeline"""
        self.embedding_service = EmbeddingService()
        
        # Create in-memory ChromaDB client
        self.client = chromadb.Client()
        self.collection = None
    
    def create_collection(self, collection_name: str = "documents") -> None:
        """
        Create or get a ChromaDB collection
        
        Args:
            collection_name: Name of the collection
        """
        try:
            # Delete existing collection if it exists
            try:
                self.client.delete_collection(name=collection_name)
            except Exception:
                pass
            
            # Create new collection
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise
    
    def add_documents(self, chunks: List[str], metadata: Optional[List[dict]] = None) -> None:
        """
        Add documents/chunks to the RAG pipeline
        
        Args:
            chunks: List of text chunks
            metadata: Optional metadata for each chunk
        """
        if not self.collection:
            self.create_collection()
        
        try:
            # Generate embeddings
            embeddings = self.embedding_service.embed_texts(chunks)
            
            # Prepare metadata
            if not metadata:
                metadata = [{"chunk_id": i} for i in range(len(chunks))]
            
            # Add to ChromaDB
            self.collection.add(
                ids=[f"chunk_{i}" for i in range(len(chunks))],
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadata
            )
            
            logger.info(f"Added {len(chunks)} chunks to pipeline")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def retrieve_similar_chunks(
        self,
        query: str,
        top_k: int = 3
    ) -> List[str]:
        """
        Retrieve the most similar chunks for a query
        
        Args:
            query: User query
            top_k: Number of top chunks to retrieve
            
        Returns:
            List of similar chunks
        """
        if not self.collection:
            logger.warning("[RAG] No collection initialized")
            return []
        
        try:
            logger.info(f"[RAG] Retrieving top {top_k} chunks for query")
            logger.info(f"[RAG] Query length: {len(query)} chars")
            
            # Generate query embedding
            query_embedding = self.embedding_service.embed_text(query)
            logger.info(f"[RAG] Query embedding generated: {len(query_embedding)} dimensions")
            
            # Query ChromaDB
            logger.info(f"[RAG] Querying ChromaDB collection...")
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            logger.info(f"[RAG] Query results received")
            
            # Extract documents
            if results and "documents" in results and len(results["documents"]) > 0:
                documents = results["documents"][0]
                logger.info(f"[RAG] ✓ Retrieved {len(documents)} chunks")
                return documents
            
            logger.warning(f"[RAG] ✗ No documents found in query results")
            return []
        except Exception as e:
            logger.error(f"[RAG] Error retrieving chunks: {str(e)}")
            logger.exception("Full traceback:")
            return []
    
    def get_context(self, query: str, top_k: int = 3) -> str:
        """
        Get formatted context for a query
        
        Args:
            query: User query
            top_k: Number of top chunks to retrieve
            
        Returns:
            Formatted context string
        """
        logger.info(f"[RAG] Getting formatted context for query: {query[:50]}...")
        
        chunks = self.retrieve_similar_chunks(query, top_k)
        
        if not chunks:
            logger.warning("[RAG] No chunks retrieved - returning empty context")
            return ""
        
        context = "\n\n".join([f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(chunks)])
        logger.info(f"[RAG] Formatted context: {len(context)} chars from {len(chunks)} chunks")
        return context
    
    def clear(self) -> None:
        """Clear the pipeline"""
        if self.collection:
            try:
                self.client.delete_collection(name=self.collection.name)
                self.collection = None
                logger.info("Cleared RAG pipeline")
            except Exception as e:
                logger.error(f"Error clearing pipeline: {str(e)}")
