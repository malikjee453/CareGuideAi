import re


def _sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]


def compress_context(query: str, results: list[dict], max_sentences_per_source: int = 4) -> list[dict]:
    """Keep only sentences most relevant to the query before generation."""
    query_terms = set(re.findall(r"[a-z0-9]+", query.lower()))
    compressed = []

    for item in results:
        scored = []
        for sentence in _sentences(item["content"]):
            terms = set(re.findall(r"[a-z0-9]+", sentence.lower()))
            overlap = len(query_terms & terms)
            scored.append((overlap, sentence))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        selected = [sentence for overlap, sentence in scored if overlap > 0][:max_sentences_per_source]
        if not selected:
            selected = _sentences(item["content"])[:2]

        updated = item.copy()
        updated["content"] = " ".join(selected)
        updated["compressed"] = True
        compressed.append(updated)

    return compressed
