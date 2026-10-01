import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from rag.embeddings import TfidfEmbeddingModel


class LocalVectorStore:
    """Small in-memory vector store for the first RAG implementation."""

    def __init__(self, chunks):
        self.chunks = chunks
        self.embedding_model = TfidfEmbeddingModel()

        texts = [chunk["content"] for chunk in chunks]

        if texts:
            self.matrix = self.embedding_model.fit_transform(texts)
        else:
            self.matrix = None

    def search(self, query: str, top_k: int = 4):
        if self.matrix is None or not self.chunks:
            return []

        query_vector = self.embedding_model.transform([query])
        scores = cosine_similarity(query_vector, self.matrix)[0]

        ranked_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for index in ranked_indices:
            score = float(scores[index])

            if score <= 0:
                continue

            item = self.chunks[index].copy()
            item["score"] = score
            results.append(item)

        return results
