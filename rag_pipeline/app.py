import streamlit as st
import time
from rag_pipeline.rag_system import RAGSystem
from rag_pipeline.pdf_utils import extract_text_from_pdf_bytes

# Page config
st.set_page_config(page_title="RAG Pipeline Tester", layout="wide")
st.title("🔍 RAG Pipeline Tester")

# Initialize session state
if 'rag' not in st.session_state:
    st.session_state.rag = None
if 'is_built' not in st.session_state:
    st.session_state.is_built = False

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    chunk_size = st.slider("Chunk Size", 400, 1500, 800)
    chunk_overlap = st.slider("Chunk Overlap", 50, 300, 100)
    retrieval_k = st.slider("Retrieval K (top documents)", 1, 20, 5)
    
    if st.button("Initialize RAG System", key="init_rag"):
        try:
            st.session_state.rag = RAGSystem(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                retrieval_k=retrieval_k
            )
            st.success("✅ RAG System initialized!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📄 Upload Document")
    
    upload_method = st.radio("Choose input method:", ["PDF File", "Text Input"])
    
    if upload_method == "PDF File":
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        if pdf_file is not None:
            if st.button("Extract & Build Index"):
                if st.session_state.rag is None:
                    st.error("❌ Initialize RAG System first!")
                else:
                    with st.spinner("Extracting PDF..."):
                        try:
                            text = extract_text_from_pdf_bytes(pdf_file.read())
                            st.session_state.pdf_text = text
                            st.success(f"✅ Extracted {len(text)} characters")
                            st.text_area("Extracted Text", text[:500] + "..." if len(text) > 500 else text, height=150, disabled=True)
                        except Exception as e:
                            st.error(f"❌ PDF Extraction Error: {str(e)}")
    else:
        text_input = st.text_area("Paste your text here:", height=200)
        if st.button("Use This Text"):
            if text_input.strip():
                st.session_state.pdf_text = text_input
                st.success("✅ Text loaded")
            else:
                st.error("❌ Please enter some text")
    
    # Build index from text
    if 'pdf_text' in st.session_state and st.button("Build RAG Index"):
        if st.session_state.rag is None:
            st.error("❌ Initialize RAG System first!")
        else:
            with st.spinner("Building RAG index... (this may take a minute)"):
                try:
                    result = st.session_state.rag.build_from_text(st.session_state.pdf_text)
                    st.session_state.is_built = True
                    
                    st.success("✅ RAG Index Built Successfully!")
                    st.json({
                        "Status": result['status'],
                        "Chunks Created": result['chunk_count'],
                        "Embedding Dimension": result['embedding_dimension'],
                        "Text Length": f"{result['text_length']} characters"
                    })
                except Exception as e:
                    st.error(f"❌ Build Error: {str(e)}")

with col2:
    st.header("🤖 Test Queries")
    
    if not st.session_state.is_built:
        st.warning("⚠️ Build the RAG index first!")
    else:
        st.success("✅ RAG Index Ready for Queries")
        
        # Query input
        query = st.text_input("Ask a question about the document:")
        
        if st.button("Search", key="search_btn"):
            if not query.strip():
                st.error("❌ Please enter a question")
            else:
                with st.spinner("Searching..."):
                    try:
                        result = st.session_state.rag.query(query, k=retrieval_k)
                        
                        if result['status'] == 'success':
                            st.success("✅ Query Successful")
                            
                            # Display context
                            st.subheader("📝 Retrieved Context")
                            st.write(result['context'])
                            
                            # Display source documents
                            st.subheader("📚 Source Documents")
                            for doc in result['source_documents']:
                                with st.expander(f"Document {doc['rank']} (Score: {doc['score']:.4f})"):
                                    st.write(doc['text'])
                            
                            # Display stats
                            st.metric("Documents Retrieved", result['retrieval_count'])
                        else:
                            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"❌ Query Error: {str(e)}")

# Test multiple queries
st.header("🧪 Test Multiple Queries")

if st.session_state.is_built:
    test_queries = [
        "What is the main topic?",
        "Explain key concepts",
        "What are the benefits?",
    ]
    
    if st.button("Run Test Queries"):
        for query in test_queries:
            if query:
                result = st.session_state.rag.query(query, k=3)
                if result['status'] == 'success':
                    st.info(f"Q: {query}")
                    st.write(f"Found {result['retrieval_count']} documents")
                    st.write("Context: " + result['context'][:200] + "...")
                    st.divider()

# Statistics
if st.session_state.is_built:
    st.header("📊 System Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Vector Count", st.session_state.rag.get_vector_count())
    
    with col2:
        st.metric("Chunk Size", st.session_state.rag.chunk_size)
    
    with col3:
        st.metric("Retrieval K", st.session_state.rag.retrieval_k)
