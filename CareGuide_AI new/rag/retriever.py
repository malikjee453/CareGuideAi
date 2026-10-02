from functools import lru_cache
from pathlib import Path

from rag.chunker import chunk_documents
from rag.loader import DEFAULT_KB_PATH, load_documents
from rag.vector_store import LocalVectorStore


@lru_cache(maxsize=1)
def get_vector_store():
    documents = load_documents(DEFAULT_KB_PATH)
    chunks = chunk_documents(documents)
    return LocalVectorStore(chunks)


def retrieve(query: str, top_k: int = 4):
    store = get_vector_store()
    return store.search(query, top_k=top_k)


def knowledge_base_status():
    documents = load_documents(DEFAULT_KB_PATH)
    chunks = chunk_documents(documents)

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "path": str(Path(DEFAULT_KB_PATH)),
    }
