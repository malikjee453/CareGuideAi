import re


def _terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def rerank(query: str, candidates: list[dict], top_k: int = 4) -> list[dict]:
    """Second-stage reranking using query-term coverage and metadata relevance."""
    query_terms = _terms(query)
    if not candidates:
        return []

    reranked = []
    for item in candidates:
        content_terms = _terms(item["content"])
        coverage = len(query_terms & content_terms) / max(len(query_terms), 1)
        score = (
            0.65 * item.get("retrieval_score", 0.0)
            + 0.25 * coverage
            + 0.10 * (1.0 if item.get("category_match") else 0.0)
        )
        updated = item.copy()
        updated["rerank_score"] = float(score)
        updated["term_coverage"] = float(coverage)
        reranked.append(updated)

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return reranked[:top_k]
