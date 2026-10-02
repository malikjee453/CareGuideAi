import re
from collections import Counter

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from rag.embeddings import TfidfEmbeddingModel
from rag.query import understand_query


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _overlap_score(query: str, document: str) -> float:
    q = Counter(_tokens(query))
    d = Counter(_tokens(document))
    if not q or not d:
        return 0.0
    matched = sum(min(count, d[token]) for token, count in q.items())
    return matched / max(sum(q.values()), 1)


def _phrase_score(query: str, document: str) -> float:
    q = " ".join(_tokens(query))
    d = " ".join(_tokens(document))
    return 1.0 if q and q in d else 0.0


class HybridRetriever:
    """Local hybrid retrieval: TF-IDF semantic proxy + lexical matching."""

    def __init__(self, chunks):
        self.chunks = chunks
        self.embedding_model = TfidfEmbeddingModel()
        texts = [chunk["content"] for chunk in chunks]
        self.matrix = self.embedding_model.fit_transform(texts) if texts else None

    def search(self, query: str, top_k: int = 10):
        if self.matrix is None or not self.chunks:
            return []

        understanding = understand_query(query)
        variants = understanding["expanded_queries"]

        tfidf_scores = np.zeros(len(self.chunks), dtype=float)
        for variant in variants:
            vector = self.embedding_model.transform([variant])
            tfidf_scores = np.maximum(tfidf_scores, cosine_similarity(vector, self.matrix)[0])

        lexical_scores = np.array(
            [_overlap_score(" ".join(variants), chunk["content"]) for chunk in self.chunks]
        )
        phrase_scores = np.array(
            [_phrase_score(query, chunk["content"]) for chunk in self.chunks]
        )

        category = understanding["category"]
        category_scores = np.array(
            [
                1.0 if category and chunk["metadata"].get("category") == category else 0.0
                for chunk in self.chunks
            ]
        )

        # Weighted candidate score. Category is a soft preference, not a hard filter.
        combined = (
            0.55 * tfidf_scores
            + 0.30 * lexical_scores
            + 0.10 * phrase_scores
            + 0.05 * category_scores
        )

        indices = np.argsort(combined)[::-1][:top_k]
        results = []
        for index in indices:
            if combined[index] <= 0:
                continue
            item = self.chunks[index].copy()
            item["retrieval_score"] = float(combined[index])
            item["tfidf_score"] = float(tfidf_scores[index])
            item["lexical_score"] = float(lexical_scores[index])
            item["category_match"] = bool(category_scores[index])
            results.append(item)

        return results
