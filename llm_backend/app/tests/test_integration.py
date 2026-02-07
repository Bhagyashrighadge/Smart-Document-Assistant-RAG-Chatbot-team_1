from app.services.ai_service import AIService

class DummyLLM:
    def generate_answer(self, question, context):
        return 'DUMMY ANSWER'

class DummyEmb:
    def __init__(self):
        pass
    def encode(self, texts):
        return [[0.01, 0.02, 0.03] for _ in texts]

class DummyRAG:
    def __init__(self):
        self.metadata = [{'text': 'doc chunk 1'},{'text':'doc chunk 2'}]
    def retrieve(self, q_vec, top_k=5):
        return [('doc chunk 1', 0.1), ('doc chunk 2', 0.2)]

class DummyMulti:
    def translate(self, text, target_lang):
        return text if target_lang == 'en' else f"[translated to {target_lang}] {text}"

def test_full_pipeline():
    service = AIService(embeddings=DummyEmb(), rag=DummyRAG(), llm=DummyLLM(), multilingual=DummyMulti())
    out = service.answer_question('What is X?', 'hi')
    assert 'answer' in out
    assert isinstance(out['source_chunks'], list)
