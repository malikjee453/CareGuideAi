"""Evidence verification agent placeholder."""


def verify_claims(answer: str, sources: list) -> dict:
    return {
        "verified": False,
        "answer": answer,
        "sources": sources,
        "note": "Evidence verification will be implemented with the RAG pipeline.",
    }
