"""Research-agent interface for approved knowledge retrieval."""

def research(query: str, retrieved_sources=None):
    sources = retrieved_sources or []
    return {"query": query, "sources": sources, "passages": [s.get("content", "") for s in sources]}
