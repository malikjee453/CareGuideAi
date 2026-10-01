"""Vector store scaffold."""


class VectorStore:
    def add(self, documents):
        raise NotImplementedError

    def search(self, query, top_k=5):
        raise NotImplementedError
