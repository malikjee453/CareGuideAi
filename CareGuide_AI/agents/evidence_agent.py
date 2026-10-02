"""EvidenceGuard: lightweight claim-level provenance checks for CareGuide AI."""

import re

_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "been", "being", "this", "that", "these", "those",
    "it", "its", "as", "by", "from", "at", "into", "can", "may", "often", "also",
    "has", "have", "had", "do", "does", "did", "than", "then", "so", "such", "some",
    "will", "would", "should", "could", "their", "there", "they", "them", "you", "your",
    "we", "our", "i", "he", "she", "his", "her", "or", "not", "only", "more", "very",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9\u0600-\u06ff]+", (text or "").lower())
        if token not in _STOPWORDS and len(token) > 2
    }


def _sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    if not cleaned:
        return []
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", cleaned) if part.strip()]


def verify_claims(answer: str, sources: list) -> dict:
    """Check each answer sentence against retrieved source content.

    This is a provenance heuristic, not a medical fact checker. It reports
    which claims have meaningful lexical support and flags weakly supported
    sentences for a second model pass.
    """
    if not answer or not sources:
        return {
            "verified": False,
            "answer": answer,
            "sources": sources or [],
            "claims": [],
            "unsupported_claims": [],
            "note": "No evidence available.",
        }

    source_blocks = [
        {"title": s.get("title", "Source"), "tokens": _tokens(s.get("content", ""))}
        for s in sources
    ]

    claims = []
    unsupported = []
    for sentence in _sentences(answer):
        claim_tokens = _tokens(sentence)
        if not claim_tokens:
            continue

        best = 0.0
        best_source = ""
        for source in source_blocks:
            score = len(claim_tokens & source["tokens"]) / max(len(claim_tokens), 1)
            if score > best:
                best = score
                best_source = source["title"]

        supported = best >= 0.22
        item = {
            "claim": sentence,
            "support_score": round(best, 3),
            "supported": supported,
            "source": best_source or "No matching source",
        }
        claims.append(item)
        if not supported:
            unsupported.append(sentence)

    verified = bool(claims) and not unsupported
    if verified:
        note = "All substantive answer sentences have meaningful lexical support in the retrieved evidence."
    else:
        note = f"{len(unsupported)} answer sentence(s) need stronger evidence support."

    return {
        "verified": verified,
        "answer": answer,
        "sources": sources,
        "claims": claims,
        "unsupported_claims": unsupported,
        "note": note,
    }
