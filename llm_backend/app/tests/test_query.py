import pytest
from app.modules.embeddings import Embeddings
from app.modules.query_processor import QueryProcessor

class DummyEmbeddings(Embeddings):
    def __init__(self):
        pass
    def encode(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]

def test_clean_and_vectorize():
    emb = DummyEmbeddings()
    qp = QueryProcessor(embeddings=emb)
    q = '  Hello   World\n'
    cleaned = qp.clean_text(q)
    assert cleaned == 'Hello World'
    vec = qp.vectorize('hello')
    assert isinstance(vec, list) or hasattr(vec, '__len__')
