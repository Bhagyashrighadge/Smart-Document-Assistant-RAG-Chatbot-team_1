from typing import List, Dict
from app.modules.query_processor import QueryProcessor
from app.modules.embeddings import Embeddings
from app.modules.rag_pipeline import RAGPipeline
from app.modules.llm_engine import LLMEngine
from app.modules.multilingual import MultilingualManager
from app.core.config import settings

class AIService:
    """Central orchestrator that integrates all modules.

    Public API: `answer_question(question: str, target_language: str)`
    """

    def __init__(self,
                 embeddings: Embeddings | None = None,
                 rag: RAGPipeline | None = None,
                 llm: LLMEngine | None = None,
                 multilingual: MultilingualManager | None = None):
        self.embeddings = embeddings or Embeddings(model_name=settings.HF_EMBEDDING_MODEL)
        self.rag = rag or RAGPipeline()
        self.llm = llm or LLMEngine()
        self.multilingual = multilingual or MultilingualManager(provider=settings.TRANSLATION_PROVIDER)
        self.query_processor = QueryProcessor(self.embeddings)

    def build_context(self, retrieved: List[tuple]) -> str:
        parts = []
        for i, (text, score) in enumerate(retrieved):
            parts.append(f"[source_{i}] {text}")
        return "\n\n".join(parts)

    def answer_question(self, question: str, target_language: str = 'en') -> Dict:
        """End-to-end answer pipeline.

        Steps:
        1. Clean + vectorize query
        2. Retrieve top-k chunks from RAG
        3. Build prompt and call LLM
        4. Translate answer if required
        5. Return answer and source chunks
        """
        cleaned = self.query_processor.clean_text(question)
        q_vec = self.query_processor.vectorize(cleaned)
        retrieved = self.rag.retrieve(q_vec, top_k=settings.TOP_K)
        context = self.build_context(retrieved)
        answer = self.llm.generate_answer(cleaned, context)
        # Translate answer if necessary
        final_answer = self.multilingual.translate(answer, target_language)
        source_chunks = [t for t, s in retrieved]
        return {"answer": final_answer, "source_chunks": source_chunks}
