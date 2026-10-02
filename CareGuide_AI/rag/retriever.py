from functools import lru_cache
from pathlib import Path

from rag.chunker import chunk_documents
from rag.loader import DEFAULT_KB_PATH, load_documents
from rag.hybrid_retriever import HybridRetriever
from rag.reranker import rerank
from rag.compressor import compress_context


@lru_cache(maxsize=1)
def get_vector_store():
    documents = load_documents(DEFAULT_KB_PATH)
    chunks = chunk_documents(documents)
    return HybridRetriever(chunks)


def retrieve(query: str, top_k: int = 4):
    candidates = get_vector_store().search(query, top_k=max(top_k * 3, 8))
    reranked = rerank(query, candidates, top_k=top_k)
    return compress_context(query, reranked)


def retrieve_with_trace(query: str, top_k: int = 4):
    candidates = get_vector_store().search(query, top_k=max(top_k * 3, 8))
    reranked = rerank(query, candidates, top_k=top_k)
    compressed = compress_context(query, reranked)
    return compressed, {
        "candidate_count": len(candidates),
        "reranked_count": len(reranked),
        "compressed_count": len(compressed),
    }


def knowledge_base_status():
    documents = load_documents(DEFAULT_KB_PATH)
    chunks = chunk_documents(documents)

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "path": str(Path(DEFAULT_KB_PATH)),
        "retrieval": "Hybrid TF-IDF + lexical matching + reranking + context compression",
    }
