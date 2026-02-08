from pydantic import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # LLM selection: 'openai' or 'local'
    LLM_PROVIDER: Literal['openai', 'local'] = 'openai'
    OPENAI_API_KEY: str | None = None
    # HuggingFace model for embeddings
    HF_EMBEDDING_MODEL: str = 'sentence-transformers/all-MiniLM-L6-v2'
    # Translation backend: 'google' or 'indic'
    TRANSLATION_PROVIDER: Literal['google', 'indic'] = 'google'
    # FAISS index path
    FAISS_INDEX_PATH: str = 'faiss_index.faiss'
    # RAG top-k
    TOP_K: int = 5

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
