import re


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def verify_claims(answer: str, sources: list) -> dict:
    """Lightweight provenance check: ensure the answer has meaningful source overlap."""
    if not answer or not sources:
        return {"verified": False, "answer": answer, "sources": sources, "note": "No evidence available."}

    answer_terms = _tokens(answer)
    source_text = " ".join(source.get("content", "") for source in sources)
    source_terms = _tokens(source_text)
    overlap = len(answer_terms & source_terms) / max(len(answer_terms), 1)

    verified = overlap >= 0.20
    note = "Answer has source-supported terminology." if verified else "Answer should be treated cautiously because source overlap is low."

    return {
        "verified": verified,
        "answer": answer,
        "sources": sources,
        "overlap": round(overlap, 3),
        "note": note,
    }
