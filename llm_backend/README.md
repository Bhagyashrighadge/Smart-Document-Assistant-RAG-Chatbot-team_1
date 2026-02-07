# Smart Document Assistant (RAG Chatbot) — Backend

This repository contains the backend for the Smart Document Assistant (RAG Chatbot).

Overview
- Modular FastAPI backend using LangChain-style RAG.
- Features: PDF ingestion (separate), embeddings, FAISS retrieval, LLM response, multilingual translation (English/Hindi/Marathi).

Repository structure (backend)
- app/
  - main.py           — FastAPI entry
  - core/config.py    — configuration + env handling
  - core/settings.py  — constants
  - modules/          — QueryProcessor, Embeddings, RAGPipeline, LLMEngine, Multilingual
  - services/ai_service.py — Orchestrator `AIService.answer_question`
  - api/chat_routes.py — `/api/chat` route
  - utils/logger.py
  - tests/             — pytest unit & integration tests

Quickstart (Windows)
1. Create virtualenv and activate
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Install dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and fill keys (e.g., `OPENAI_API_KEY`)
4. Run the app
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: Chat
- POST /api/chat
- Body JSON:
  {
    "question": "...",
    "language": "en"  // 'en' | 'hi' | 'mr'
  }
- Response JSON:
  {
    "answer": "...",
    "source_chunks": ["...", ...]
  }

Notes and integration
- FAISS index: The `RAGPipeline` expects a FAISS index at `FAISS_INDEX_PATH` configured in `.env`. If no index is present, retrieval returns empty list — ingest pipeline should build index and metadata (not included here).
- Embeddings: `app.modules.embeddings.Embeddings` uses `sentence-transformers` model configured by `HF_EMBEDDING_MODEL` in `.env`.
- LLM: `app.modules.llm_engine.LLMEngine` supports `openai` by default using `OPENAI_API_KEY`. Local LLMs can be integrated by replacing implementation in `llm_engine.py`.
- Multilingual: `app.modules.multilingual.MultilingualManager` uses a provider strategy (`google` or `indic`) and provides `detect_language` and `translate`.

Running tests
```powershell
cd backend
pytest -q
```

Postman
- Import the provided `postman_collection.json` file in Postman to test `/api/chat`.

Next steps for teammates
- Implement document ingestion: chunking, encoding via `Embeddings.encode`, building FAISS index and `metadata` mapping, then call `RAGPipeline.load_metadata()`.
- Plug a real translation backend for `IndicNLPStrategy` or configure Google Cloud Translate.
- Replace `LLMEngine` local placeholder with a local LLM client (e.g., LlamaCPP, Ollama) if required.

Contact
- If you want, I can add an ingestion helper script, or wire CI for tests. Request next step.
