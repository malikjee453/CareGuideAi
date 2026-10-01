def chunk_text(text: str, chunk_size: int = 900, overlap: int = 150):
    """Split text into overlapping word-based chunks."""
    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))

        if end >= len(words):
            break

        start = max(end - overlap, start + 1)

    return chunks


def chunk_documents(
    documents,
    chunk_size: int = 900,
    overlap: int = 150,
):
    """Create chunks while preserving source metadata."""
    chunks = []

    for document in documents:
        parts = chunk_text(
            document["content"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for index, part in enumerate(parts):
            chunks.append(
                {
                    "content": part,
                    "metadata": document["metadata"].copy(),
                    "chunk_id": index,
                    "path": document["path"],
                }
            )

    return chunks
