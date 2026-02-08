import numpy as np
from app.modules.rag_pipeline import RAGPipeline

class DummyIndex:
    def __init__(self, n, dim):
        self.n = n
        self.dim = dim
    def search(self, q, k):
        # return distances and indices
        D = [[0.1 * i for i in range(k)]]
        I = [[i for i in range(k)]]
        return np.array(D, dtype=float), np.array(I, dtype=int)

def test_retrieve_with_no_index(monkeypatch):
    rp = RAGPipeline(index_path='nonexistent.faiss')
    rp.index = DummyIndex(3, 3)
    rp.load_metadata([{'text':'a'},{'text':'b'},{'text':'c'}])
    q = np.array([0.1,0.2,0.3])
    res = rp.retrieve(q, top_k=2)
    assert isinstance(res, list)
    assert len(res) == 2
