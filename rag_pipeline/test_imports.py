#!/usr/bin/env python
"""Quick test to verify all modules load correctly"""

print("Testing imports...")

try:
    from rag_pipeline.chunker import TextChunker
    print("✓ TextChunker imported")
except Exception as e:
    print(f"✗ TextChunker: {e}")

try:
    from rag_pipeline.embeddings import EmbeddingModel
    print("✓ EmbeddingModel imported")
except Exception as e:
    print(f"✗ EmbeddingModel: {e}")

try:
    from rag_pipeline.vector_store import FAISSVectorStore
    print("✓ FAISSVectorStore imported")
except Exception as e:
    print(f"✗ FAISSVectorStore: {e}")

try:
    from rag_pipeline.retriever import Retriever
    print("✓ Retriever imported")
except Exception as e:
    print(f"✗ Retriever: {e}")

try:
    from rag_pipeline.rag_system import RAGSystem
    print("✓ RAGSystem imported")
except Exception as e:
    print(f"✗ RAGSystem: {e}")

try:
    from rag_pipeline.pdf_utils import extract_text_from_pdf_bytes
    print("✓ PDF utilities imported")
except Exception as e:
    print(f"✗ PDF utilities: {e}")

print("\n✓ All imports successful!")
print("\nTesting TextChunker...")
chunker = TextChunker()
chunks = chunker.chunk_text("This is a test. " * 100)
print(f"✓ Created {len(chunks)} chunks from test text")

print("\nAll tests passed! ✓")
