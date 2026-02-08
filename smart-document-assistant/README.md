# AskDocAI - Professional AI-Powered Document Assistant

A complete end-to-end RAG (Retrieval-Augmented Generation) system for intelligent PDF Q&A with multilingual support.

## Features

✨ **Core Features:**
- 📄 Upload and process PDF documents
- 💬 Ask questions about your documents in natural language
- 📊 Get intelligent, context-aware answers
- 🌐 Multilingual support (English, Hindi, Marathi)
- 🤖 Powered by DeepSeek AI with advanced embeddings
- ⚡ Lightning-fast semantic search and retrieval
- 🎨 Professional UI with light/dark mode
- 📱 Responsive design for all devices

## Tech Stack

### Frontend
- **React.js** (with Vite) - Modern UI framework
- **Tailwind CSS** - Professional styling system
- **Axios** - API integration
- **React Router** - Client-side navigation
- **Theme Context** - Light/Dark mode support

### Backend
- **Python FastAPI** - RESTful API server
- **LangChain** - RAG orchestration and chains
- **ChromaDB** - Vector database (in-memory)
- **Sentence-Transformers** - Advanced embeddings
- **pdfplumber** - PDF text extraction
- **DeepSeek API** - Large language model
- **Google Translate** - Multilingual translation

## Project Structure

```
smart-document-assistant/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── requirements.txt         # Python dependencies
│   ├── run_server.py           # Server runner
│   ├── .env                    # Environment configuration
│   ├── api/
│   │   ├── routes.py           # API endpoints
│   │   ├── schemas.py          # Pydantic schemas
│   │   └── utils.py            # Utility functions
│   ├── services/
│   │   ├── pdf_processor.py    # PDF parsing
│   │   ├── rag_pipeline.py     # RAG orchestration
│   │   ├── embedding_service.py # Vector embeddings
│   │   ├── deepseek_service.py # LLM integration
│   │   ├── language_detector.py # Language detection
│   │   ├── translator.py       # Multilingual support
│   │   └── mock_responses.py  # Testing utilities
│   └── models/
│       ├── session_store.py    # Session management
│       └── __init__.py
│
├── frontend/
│   ├── package.json            # Node dependencies
│   ├── tailwind.config.js      # Tailwind configuration
│   ├── vite.config.js          # Vite build configuration
│   ├── index.html              # HTML entry point
│   └── src/
│       ├── App.jsx             # Root component
│       ├── main.jsx            # React entry
│       ├── index.css           # Global styles
│       ├── components/
│       │   ├── Navbar.jsx      # Navigation bar
│       │   ├── Upload.jsx      # PDF upload component
│       │   ├── Chat.jsx        # Chat interface
│       │   ├── LanguageSelector.jsx # Language switcher
│       │   └── Footer.jsx      # Footer section
│       ├── context/
│       │   ├── LanguageContext.jsx # Language state
│       │   └── ThemeContext.jsx    # Light/Dark mode
│       ├── pages/
│       │   ├── Home.jsx        # Landing page
│       │   └── ChatPage.jsx    # Main chat interface
│       └── services/
│           └── api.js          # API client

## Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- DeepSeek API key ([Get one here](https://api.deepseek.com))

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
# Edit .env file and add your DeepSeek API key
DEEPSEEK_API_KEY=your_api_key_here
```

5. Run backend:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Usage

1. **Start both servers** (in separate terminals):
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. **Open browser**: `http://localhost:5173`

3. **Upload PDF**: Click "Get Started" and upload your PDF document

4. **Ask Questions**: Type questions about the document in the chat

5. **Change Language**: Select English (EN), Hindi (HI), or Marathi (MR)

6. **Get Answers**: Receive intelligent answers powered by DeepSeek AI

## API Endpoints

### POST `/api/upload-pdf`
Upload a PDF file and initialize a document session.

**Request:**
```
multipart/form-data
- file: PDF file
```

**Response:**
```json
{
  "success": true,
  "session_id": "uuid",
  "message": "Successfully processed 'document.pdf'",
  "document_name": "document.pdf"
}
```

### POST `/api/ask-question`
Ask a question about the uploaded document.

**Request:**
```json
{
  "session_id": "uuid",
  "question": "What is the main topic?",
  "language": "en"
}
```

**Response:**
```json
{
  "success": true,
  "answer": "The document discusses...",
  "original_answer": "The document discusses...",
  "language": "en"
}
```

### POST `/api/translate`
Translate text to another language.

**Request:**
```json
{
  "text": "Hello world",
  "target_language": "hi"
}
```

**Response:**
```json
{
  "success": true,
  "original_text": "Hello world",
  "translated_text": "नमस्ते दुनिया",
  "target_language": "hi"
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "All services operational"
}
```

### GET `/api/session/{session_id}`
Get session information including chat history.

### DELETE `/api/session/{session_id}`
Delete a session.

## How the RAG Pipeline Works

1. **PDF Processing**: Extract text from uploaded PDF
2. **Text Cleaning**: Remove extra whitespace and normalize content
3. **Chunking**: Split text into overlapping chunks
4. **Embedding**: Generate embeddings using Sentence Transformers
5. **Indexing**: Store embeddings in ChromaDB (in-memory)
6. **Retrieval**: Find semantically similar chunks for user query
7. **Generation**: Send context + query to DeepSeek API
8. **Translation**: Translate response to requested language

## Supported Languages

- 🇬🇧 **English** (en)
- 🇮🇳 **Hindi** (hi)
- 🇮🇳 **Marathi** (mr)

Translation is done using MyMemory Translate API (free, no key required).

## Error Handling

The application includes comprehensive error handling:

- **File validation**: Checks PDF format and size
- **API validation**: Validates all request parameters
- **Exception handling**: Graceful error messages for users
- **Session management**: Automatic cleanup on errors

## Performance Optimizations

- In-memory vector store (no I/O overhead)
- Lazy initialization of services
- GZIP compression for responses
- Efficient text chunking with overlap
- Session-based storage (lightweight)

## Limitations & Future Improvements

### Current Limitations
- No persistent storage (session-based only)
- Single-machine deployment (no clustering)
- In-memory vector store limited by RAM

### Potential Improvements
- Add database support (PostgreSQL + pgvector)
- Support more languages
- Add file type support (DOCX, TXT, etc.)
- Implement user authentication
- Add document history/bookmarking
- Multi-file RAG support
- Custom embedding models
- Response caching

## Configuration

### Environment Variables

All configuration is in `backend/.env`:

```env
DEEPSEEK_API_KEY=your_api_key_here
```

### Backend Configuration (main.py)

Modify CORS origins:
```python
allow_origins=["http://localhost:5173", "*"],
```

### Frontend Configuration (vite.config.js)

Modify API base URL:
```js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
  }
}
```

## Building for Production

### Backend
```bash
cd backend
pip install -r requirements.txt
# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Frontend
```bash
cd frontend
npm run build
# Output in frontend/dist/
# Serve with any static host (Vercel, Netlify, etc.)
```

## Troubleshooting

### "DEEPSEEK_API_KEY not found"
- Ensure `.env` file exists in backend directory
- Add your API key to the .env file
- Restart the backend server

### "PDF extraction failed"
- Ensure PDF file is not corrupted
- Try with a different PDF file
- Check file size is under 50MB

### "Connection refused"
- Ensure backend is running on port 8000
- Ensure frontend is running on port 5173
- Check firewall settings

### "No relevant information found"
- Upload a document with more content
- Ask more specific questions
- Check if the question is related to the document

## Testing the Full Flow

```bash
# 1. Start backend
cd backend
uvicorn main:app --reload

# 2. Start frontend (in new terminal)
cd frontend
npm run dev

# 3. Open http://localhost:5173

# 4. Upload a PDF (use any sample PDF)

# 5. Ask questions:
# - "What is this document about?"
# - "Summarize the main points"
# - "List key findings"

# 6. Switch language to Hindi (हिंदी) or Marathi (मराठी)

# 7. Verify you get translated answers
```

## Support & Documentation

- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc`
- **GitHub**: [Your Repository]

## License

MIT License - feel free to use for personal and commercial projects

## Contributors

- Built with ❤️ for the multilingual community
- Powered by DeepSeek AI

---

**Happy document analysis! 🚀**
