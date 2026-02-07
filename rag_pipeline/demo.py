from rag_pipeline.rag_system import RAGSystem

SAMPLE_TEXT = """
Artificial Intelligence (AI) is transforming industries worldwide. Machine Learning, 
a subset of AI, enables computers to learn from data without explicit programming. 
Deep Learning uses neural networks with multiple layers to process complex patterns.

Natural Language Processing (NLP) allows machines to understand and generate human language.
Text classification, sentiment analysis, and machine translation are key NLP applications.

Computer Vision enables machines to interpret visual information from images and videos.
Applications include object detection, facial recognition, and autonomous vehicles.

Data Science combines statistics, programming, and domain expertise to extract insights from data.

Cloud Computing provides on-demand access to computing resources over the internet.
Major providers include AWS, Google Cloud, and Microsoft Azure.

Cybersecurity protects information systems from digital attacks and unauthorized access.

The Internet of Things (IoT) connects physical devices to the internet for data collection.

Blockchain technology provides decentralized and immutable record-keeping.

DevOps combines development and operations for faster, more reliable software delivery.

Quantum Computing harnesses quantum mechanics for powerful computation.

Edge Computing brings processing closer to data sources for reduced latency.

Microservices architecture breaks applications into small, independent services.
"""

def main():
    print("\n" + "="*50)
    print("RAG PIPELINE DEMO")
    print("="*50 + "\n")
    
    try:
        # Initialize
        print("1. Initializing RAG System...")
        rag = RAGSystem(chunk_size=800, chunk_overlap=100)
        print("✓ Initialized\n")
        
        # Build
        print("2. Building index from text...")
        result = rag.build_from_text(SAMPLE_TEXT)
        print(f"✓ Built with {result['chunk_count']} chunks\n")
        
        # Query
        print("3. Testing queries...")
        questions = [
            "What is Machine Learning?",
            "Explain AI applications",
            "What is cloud computing?"
        ]
        
        for q in questions:
            print(f"\nQ: {q}")
            result = rag.query(q, k=3)
            print(f"Found {result['retrieval_count']} documents")
            print(f"Context: {result['context'][:150]}...")
        
        print("\n" + "="*50)
        print("✓ DEMO COMPLETED SUCCESSFULLY")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

