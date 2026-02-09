# RAG Pipeline - Visual Architecture & Component Mapping

## System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND (React + Vite)                        │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │  Home Page      │  │  Chat Page       │  │  Upload Handler  │       │
│  │                 │  │                  │  │                  │       │
│  │  Shows RAG      │  │  Question input  │  │  PDF upload UI   │       │
│  │  overview       │  │  Answer display  │  │  Progress bar    │       │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬─────────┘       │
│           │                    │                      │                  │
└───────────┼────────────────────┼──────────────────────┼────────────────┘
            │                    │                      │
            │  /api/ask-question │                      │ /api/upload-pdf
            │         POST       │                      │     POST
            │                    │                      │
            ▼                    ▼                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      FASTAPI ROUTER LAYER                                │
│  ┌───────────────────────┐        ┌─────────────────────────────────┐  │
│  │  Request Handlers     │        │  Response Formatters            │  │
│  │  - Input validation   │        │  - JSON serialization           │  │
│  │  - File upload mgmt   │        │  - Error handling               │  │
│  │  - Session routing    │        │  - Timestamp addition           │  │
│  └───────────────────────┘        └─────────────────────────────────┘  │
└───────────┬──────────────────────────────────────────────────┬──────────┘
            │                                                  │
            │ upload_pdf()                                     │ ask_question()
            │                                                  │
            ▼                                                  ▼
┌─────────────────────────────────┐        ┌──────────────────────────────┐
│  PDF PROCESSING PIPELINE        │        │  QUESTION ANSWERING PIPELINE │
│                                 │        │                              │
│  ┌────────────────────────────┐ │        │ ┌─────────────────────────┐ │
│  │ 1. File Validation         │ │        │ │ 1. Session Validation   │ │
│  │    - Check if actual PDF   │ │        │ │    - Verify session_id  │ │
│  │    - Validate MIME type    │ │        │ │    - Check RAG pipeline │ │
│  └────────────────────────────┘ │        │ └─────────────────────────┘ │
│           │                      │        │           │                 │
│           ▼                      │        │           ▼                 │
│  ┌────────────────────────────┐ │        │ ┌─────────────────────────┐ │
│  │ 2. PDF Text Extraction     │ │        │ │ 2. Question Embedding   │ │
│  │    - Load with pdfplumber  │ │        │ │    - Sentence-Transform │ │
│  │    - Iterate through pages │ │        │ │    - Get 384-d vector   │ │
│  │    - Concatenate text      │ │        │ └─────────────────────────┘ │
│  └────────────────────────────┘ │        │           │                 │
│           │                      │        │           ▼                 │
│           ▼                      │        │ ┌─────────────────────────┐ │
│  ┌────────────────────────────┐ │        │ │ 3. Semantic Search      │ │
│  │ 3. Text Cleaning           │ │        │ │    - Query ChromaDB     │ │
│  │    - Remove extra spaces   │ │        │ │    - Cosine similarity  │ │
│  │    - Normalize newlines    │ │        │ │    - Retrieve top-k     │ │
│  │    - Clean artifacts       │ │        │ └─────────────────────────┘ │
│  └────────────────────────────┘ │        │           │                 │
│           │                      │        │           ▼                 │
│           ▼                      │        │ ┌─────────────────────────┐ │
│  ┌────────────────────────────┐ │        │ │ 4. Context Assembly     │ │
│  │ 4. Text Chunking           │ │        │ │    - Concatenate chunks │ │
│  │    - Chunk: 500 characters │ │        │ │    - Add delimiters     │ │
│  │    - Overlap: 50 characters│ │        │ │    - Format for prompt  │ │
│  │    - Preserve context      │ │        │ └─────────────────────────┘ │
│  └────────────────────────────┘ │        │           │                 │
│           │                      │        │           ▼                 │
│           ▼                      │        │ ┌─────────────────────────┐ │
│  ┌────────────────────────────┐ │        │ │ 5. LLM Query            │ │
│  │ 5. Embedding Generation    │ │        │ │    - Call DeepSeek API  │ │
│  │    - Load model once       │ │        │ │    - With document ctx  │ │
│  │    - Batch encode chunks   │ │        │ │    - Get response       │ │
│  │    - 384-dimensional vecs  │ │        │ └─────────────────────────┘ │
│  └────────────────────────────┘ │        │           │                 │
│           │                      │        │           ▼                 │
│           ▼                      │        │ ┌─────────────────────────┐ │
│  ┌────────────────────────────┐ │        │ │ 6. Response Validation  │ │
│  │ 6. ChromaDB Storage        │ │        │ │    - Detect language    │ │
│  │    - Create collection     │ │        │ │    - Verify accuracy    │ │
│  │    - Add documents         │ │        │ │    - Calculate confidence
│  │    - Build HNSW index      │ │        │ └─────────────────────────┘ │
│  └────────────────────────────┘ │        │           │                 │
│           │                      │        │           ▼                 │
│           ▼                      │        │ ┌─────────────────────────┐ │
│  ┌────────────────────────────┐ │        │ │ 7. Session History Save │ │
│  │ 7. Response Return         │ │        │ │    - Add to chatlog     │ │
│  │    - Session ID            │ │        │ │    - Enable follow-ups  │ │
│  │    - Success status        │ │        │ └─────────────────────────┘ │
│  │    - Document metadata     │ │        │           │                 │
│  └────────────────────────────┘ │        │           ▼                 │
│                                 │        │  Response JSON Return        │
└────────────┬────────────────────┘        └──────────────────────────────┘
             │                                        │
             └────────────────┬───────────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │  SESSION STORE (RAM) │
                    │  - In-memory dict    │
                    │  - Per-user isolated │
                    │  - Message history   │
                    │  - Metadata storage  │
                    └──────────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │    RAG PIPELINE      │
                    │  - ChromaDB Client   │
                    │  - Vector Store      │
                    │  - HNSW Index        │
                    │  - Query Interface   │
                    └──────────────────────┘
                              │
                              ▼
                ┌─────────────────────────────┐
                │   CHROMADB (Vector DB)      │
                │                             │
                │  Collections (per session): │
                │  ├─ session_abc123          │
                │  │  ├─ chunk_0 embedding   │
                │  │  ├─ chunk_1 embedding   │
                │  │  └─ chunk_N embedding   │
                │  ├─ session_xyz789          │
                │  └─ ...                    │
                │                             │
                │  Index Method: HNSW        │
                │  Similarity: Cosine        │
                │  Speed: <10ms search       │
                └─────────────────────────────┘
                              │
                              ▼
                ┌─────────────────────────────┐
                │  EMBEDDING SERVICE          │
                │                             │
                │  Model: all-MiniLM-L6-v2   │
                │  ├─ Dimensions: 384        │
                │  ├─ Languages: 100+        │
                │  ├─ Speed: 10k/sec         │
                │  └─ Size: 135MB            │
                └─────────────────────────────┘
                              │
                              ▼
                ┌─────────────────────────────┐
                │   EXTERNAL SERVICES         │
                │                             │
                │  ┌──────────────────────┐  │
                │  │  DeepSeek API        │  │
                │  │  - Chat Endpoint     │  │
                │  │  - Model: deepseek*  │  │
                │  │  - Language: 100+    │  │
                │  │  - Speed: 1-5s/req   │  │
                │  └──────────────────────┘  │
                │                             │
                │  ┌──────────────────────┐  │
                │  │  Language Detector   │  │
                │  │  - langdetect lib    │  │
                │  │  - 55+ languages     │  │
                │  │  - Used for validate │  │
                │  └──────────────────────┘  │
                └─────────────────────────────┘
```

---

## Component Interaction Map

### Data Flow for PDF Upload

```
User selects PDF file
        │
        ▼
Frontend: Upload.jsx
        │
        ├─ Validate file type (PDF)
        ├─ Show progress bar
        │
        └─→ POST /api/upload-pdf
                │
                ▼
        FastAPI Backend
                │
                ├─ File validation
                ├─ Temporary save
                │
                ▼
        PDFProcessor.extract_text()
                │
                ├─ pdfplumber.open()
                ├─ Iterate pages
                ├─ extract_text()
                │
                ▼
        Raw text (with formatting issues)
                │
                ▼
        PDFProcessor.clean_text()
                │
                ├─ Strip whitespace
                ├─ Remove duplicates
                ├─ Normalize encoding
                │
                ▼
        Clean text
                │
                ▼
        PDFProcessor.chunk_text()
                │
                ├─ Split 500 chars
                ├─ Add 50 char overlap
                ├─ Preserve context
                │
                ▼
        List[chunks]
                │
                ▼
        RAGPipeline.create_collection()
                │
                ├─ Create "session_{id}"
                ├─ Configure cosine metric
                ├─ Setup HNSW index
                │
                ▼
        EmbeddingService.embed_texts()
                │
                ├─ Load model
                ├─ Batch encode chunks
                ├─ Generate 384-d vectors
                │
                ▼
        List[embeddings]
                │
                ▼
        ChromaDB.add()
                │
                ├─ Store embeddings
                ├─ Store documents
                ├─ Store metadata
                ├─ Build index
                │
                ▼
        Response: 200 OK
        {
            "session_id": "abc-123",
            "document_name": "file.pdf",
            "chunks_count": 45
        }
                │
                ▼
        Frontend: Display session_id
        User ready to ask questions
```

---

### Data Flow for Question Answering

```
User types question
        │
        ▼
Frontend: Chat.jsx
        │
        ├─ Get session_id from storage
        ├─ Get question text
        ├─ Get language preference
        │
        └─→ POST /api/ask-question
                {
                    "session_id": "abc-123",
                    "question": "What is...?",
                    "language": "en"
                }
                │
                ▼
        FastAPI Backend
                │
                ├─ Validate session exists
                ├─ Get RAGPipeline from store
                │
                ▼
        EmbeddingService.embed_single()
                │
                ├─ Load same model (cached)
                ├─ Encode question text
                ├─ Get 384-d vector
                │
                ▼
        Question embedding
                │
                ▼
        RAGPipeline.retrieve_similar_chunks()
                │
                ├─ ChromaDB query
                ├─ Cosine similarity search
                ├─ HNSW navigation
                ├─ Rank by score
                │
                ▼
        Top-3 chunks (highest similarity)
                │
                ├─ Chunk A: similarity 0.92
                ├─ Chunk B: similarity 0.87
                └─ Chunk C: similarity 0.78
                │
                ▼
        RAGPipeline.get_context()
                │
                ├─ Format chunks
                ├─ Add separators
                ├─ Create context window
                │
                ▼
        Context string (formatted)
        <DOCUMENT_CONTEXT>
        Chunk A text...
        Chunk B text...
        Chunk C text...
        </DOCUMENT_CONTEXT>
                │
                ▼
        DeepSeekService.generate_response()
                │
                ├─ Build system prompt
                ├─ Build user prompt with context
                ├─ Call DeepSeek API
                ├─ Stream response
                │
                ▼
        LLM Response
        "The answer is..."
                │
                ▼
        LanguageDetector.is_response_in_language()
                │
                ├─ Detect response language
                ├─ Compare with requested
                ├─ Calculate confidence
                │
                ▼
        Response validation result
        {
            "is_valid": true,
            "detected_language": "en",
            "confidence": 0.98
        }
                │
                ▼
        SessionStore.add_message()
                │
                ├─ Store question
                ├─ Store answer
                ├─ Save timestamp
                │
                ▼
        Response: 200 OK
        {
            "success": true,
            "answer": "The answer is...",
            "language": "en",
            "confidence": 0.98,
            "timestamp": "2026-02-09T08:20:45Z"
        }
                │
                ▼
        Frontend: Chat.jsx
        ├─ Display answer
        ├─ Enable follow-up question
        └─ Show language badge
```

---

## Module Dependency Graph

```
┌────────────────────────────────────────┐
│  FRONTEND LAYER                        │
│                                        │
│  ├─ App.jsx (main entry)               │
│  │  └─ uses: React Router              │
│  │                                     │
│  ├─ ChatPage.jsx (chat interface)      │
│  │  └─ uses: Chat.jsx                  │
│  │           Upload.jsx                │
│  │           LanguageSelector.jsx      │
│  │                                     │
│  ├─ services/api.js (HTTP calls)       │
│  │  └─ uses: Fetch API                 │
│  │           axios (optional)          │
│  │                                     │
│  └─ context/ (state management)        │
│     ├─ LanguageContext.jsx             │
│     └─ ThemeContext.jsx                │
│                                        │
└───────────────────┬──────────────────┘
                    │
        HTTP (REST API)
                    │
                    ▼
┌────────────────────────────────────────┐
│  FASTAPI ROUTER (api/routes.py)        │
│                                        │
│  ├─ @app.get("/health")                │
│  ├─ @app.post("/upload-pdf")           │
│  ├─ @app.post("/ask-question")         │
│  ├─ @app.get("/session/{session_id}")  │
│  └─ @app.post("/translate")            │
│                                        │
└───────────────────┬──────────────────┘
          │         │         │
          ▼         ▼         ▼
    ┌─────────────────────────────────┐
    │  SERVICE LAYER                  │
    │                                 │
    │  ├─ PDFProcessor                │
    │  │  └─ uses: pdfplumber        │
    │  │                             │
    │  ├─ EmbeddingService           │
    │  │  └─ uses: Sentence-Transform│
    │  │           sentence_transformers
    │  │                             │
    │  ├─ RAGPipeline                │
    │  │  └─ uses: ChromaDB          │
    │  │           EmbeddingService  │
    │  │                             │
    │  ├─ DeepSeekService            │
    │  │  └─ uses: httpx             │
    │  │           DeepSeek API      │
    │  │                             │
    │  ├─ LanguageDetector           │
    │  │  └─ uses: langdetect        │
    │  │                             │
    │  ├─ Translator                 │
    │  │  └─ uses: Google Translate  │
    │  │           (optional)        │
    │  │                             │
    │  └─ MockResponses              │
    │     └─ fallback data           │
    │                                 │
    └───────────────────┬─────────────┘
                        │
                        ▼
    ┌─────────────────────────────────┐
    │  DATA LAYER                     │
    │                                 │
    │  ├─ SessionStore (models/)      │
    │  │  └─ In-memory storage        │
    │  │                             │
    │  ├─ ChromaDB                    │
    │  │  └─ Vector persistence       │
    │  │                             │
    │  └─ schemas.py (Pydantic)       │
    │     └─ Request/Response models  │
    │                                 │
    └─────────────────────────────────┘
```

---

## Session Lifecycle

```
┌─────────────────────────────────────────┐
│  SESSION CREATED                        │
│  session_id = UUID4()                   │
│  timestamp = now()                      │
│  state = "empty"                        │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  PDF UPLOADED                           │
│  - RAGPipeline instance created         │
│  - ChromaDB collection created          │
│  - Embeddings generated & stored        │
│  state = "ready"                        │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  MULTIPLE QUESTIONS                     │
│  - Each question embedded               │
│  - Semantic search executed             │
│  - Context retrieved                    │
│  - Answer generated                     │
│  - Message history updated              │
│  state = "active"                       │
└────────┬────────────────────────────────┘
         │
         ├─ Follow-up Q1 ──────┐
         │                     │
         ├─ Follow-up Q2 ──────┼────┐
         │                     │    │
         ├─ Follow-up Q3 ──────┼────┼────┐
         │                     │    │    │
         ▼                     ▼    ▼    ▼
┌─────────────────────────────────────────┐
│  SESSION ENDED                          │
│  - All messages saved                   │
│  - RAGPipeline memory freed             │
│  - Session history available            │
│  state = "closed"                       │
└─────────────────────────────────────────┘
```

---

## File Organization & Dependencies

```
smart-document-assistant/
│
├── backend/
│   │
│   ├── main.py
│   │   └─ imports: FastAPI, uvicorn
│   │
│   ├── run_server.py
│   │   └─ imports: main.py
│   │
│   ├── api/
│   │   │
│   │   ├── routes.py (★ ENTRY POINT)
│   │   │   ├─ imports: FastAPI, File, UploadFile
│   │   │   ├─ imports: PDFProcessor
│   │   │   ├─ imports: RAGPipeline
│   │   │   ├─ imports: EmbeddingService
│   │   │   ├─ imports: DeepSeekService
│   │   │   ├─ imports: LanguageDetector
│   │   │   ├─ imports: SessionStore
│   │   │   └─ imports: schemas
│   │   │
│   │   ├── schemas.py
│   │   │   └─ defines: Pydantic request/response models
│   │   │
│   │   └── utils.py
│   │       └─ utility functions
│   │
│   ├── services/
│   │   │
│   │   ├── pdf_processor.py
│   │   │   └─ imports: pdfplumber
│   │   │
│   │   ├── embedding_service.py (★ CRITICAL)
│   │   │   └─ imports: sentence_transformers
│   │   │           numpy
│   │   │
│   │   ├── rag_pipeline.py (★ CORE)
│   │   │   ├─ imports: chromadb
│   │   │   ├─ imports: EmbeddingService
│   │   │   └─ manages: Vector store + Retrieval
│   │   │
│   │   ├── deepseek_service.py
│   │   │   └─ imports: httpx (async HTTP)
│   │   │           os (env vars)
│   │   │
│   │   ├── language_detector.py
│   │   │   └─ imports: langdetect
│   │   │
│   │   ├── translator.py
│   │   │   └─ imports: google.cloud.translate_v2 (optional)
│   │   │
│   │   └── mock_responses.py
│   │       └─ fallback data for testing
│   │
│   ├── models/
│   │   │
│   │   ├── session_store.py
│   │   │   └─ manages: In-memory session storage
│   │   │
│   │   └── __init__.py
│   │
│   └── requirements.txt
│       ├─ fastapi
│       ├─ uvicorn
│       ├─ pydantic
│       ├─ pdfplumber
│       ├─ sentence-transformers
│       ├─ chromadb
│       ├─ langdetect
│       ├─ numpy
│       └─ ... (15+ total)
│
└── frontend/
    │
    ├── index.html
    ├── main.jsx (React entry)
    │   └─ imports: App.jsx
    │
    ├── App.jsx (★ MAIN APP)
    │   ├─ Router setup
    │   ├─ imports: ChatPage
    │   ├─ imports: Home
    │   ├─ imports: LanguageContext
    │   └─ imports: ThemeContext
    │
    ├── pages/
    │   │
    │   ├── ChatPage.jsx
    │   │   ├─ imports: Chat.jsx
    │   │   ├─ imports: Upload.jsx
    │   │   ├─ imports: LanguageSelector.jsx
    │   │   └─ imports: api.js
    │   │
    │   └── Home.jsx
    │       ├─ Landing page
    │       └─ Shows RAG overview
    │
    ├── components/
    │   ├── Chat.jsx
    │   │   └─ imports: api.js
    │   ├── Upload.jsx
    │   │   └─ imports: api.js
    │   ├── Navbar.jsx
    │   ├── Footer.jsx
    │   ├── LanguageSelector.jsx
    │   └── PDFAnalysis.jsx (custom SVG)
    │
    ├── context/
    │   ├── LanguageContext.jsx
    │   │   └─ manages: language state
    │   └── ThemeContext.jsx
    │       └─ manages: dark/light theme
    │
    ├── services/
    │   └── api.js (★ HTTP CALLS)
    │       ├─ axios config
    │       ├─ uploadPDF()
    │       ├─ askQuestion()
    │       └─ getSessionInfo()
    │
    └── package.json
        ├─ react
        ├─ react-router-dom
        ├─ axios
        ├─ tailwind
        └─ ... (dependencies)
```

---

## Request-Response Cycle with Latency

```
┌──────────────────────────────────────────────────────┐
│  UPLOAD PDF REQUEST                                  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  User File Selection        0ms  ←─ UI interaction │
│  File Validation            10ms ←─ Size + type    │
│  HTTP POST                  20ms ←─ Network        │
│  ────────────────────────────────────────────────  │
│  File Save                  50ms ←─ Disk I/O       │
│  PDF Extraction             300ms ←─ pdfplumber    │
│  Text Cleaning              50ms ←─ Regex ops     │
│  Text Chunking              100ms ←─ Split ops    │
│  Embedding Generation       2000ms ←─ Model       │
│  ChromaDB Storage           200ms ←─ Index build  │
│  ────────────────────────────────────────────────  │
│  JSON Response              10ms ←─ Serialization │
│  ────────────────────────────────────────────────  │
│  TOTAL: ~2.7 seconds                               │
│                                                      │
│  User sees: "Upload complete!" ✓                   │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  QUESTION REQUEST                                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  User Types + Hit Send      0ms ←─ UI interaction │
│  HTTP POST                  20ms ←─ Network        │
│  ────────────────────────────────────────────────  │
│  Question Embedding         100ms ←─ Model        │
│  ChromaDB Vector Search     50ms ←─ HNSW query    │
│  Context Assembly           10ms ←─ String ops   │
│  DeepSeek API Call          3000ms ←─ LLM        │
│  Language Validation        50ms ←─ Detection    │
│  Session History Save       20ms ←─ Storage      │
│  ────────────────────────────────────────────────  │
│  JSON Response              10ms ←─ Serialization │
│  ────────────────────────────────────────────────  │
│  TOTAL: ~3.2 seconds                               │
│                                                      │
│  User sees: "Answer displayed" ✓                   │
└──────────────────────────────────────────────────────┘
```

---

## This is Your RAG Pipeline!

You've built a system that:
- ✅ Extracts knowledge from PDFs
- ✅ Converts text to semantic embeddings
- ✅ Stores vectors in production database
- ✅ Retrieves relevant context via similarity
- ✅ Generates grounded answers with LLM
- ✅ Validates and formats responses
- ✅ Supports 100+ languages natively
- ✅ Isolates sessions for multi-user safety

**Congratulations on the implementation!** 🎉
