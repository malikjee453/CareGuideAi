"""Response agent assembles the final answer and provenance."""

def build_response(answer: str, sources: list | None = None, evidence: dict | None = None) -> dict:
    return {"answer": answer, "sources": sources or [], "evidence": evidence or {}}
