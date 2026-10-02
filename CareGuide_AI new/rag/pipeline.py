from agents.llm_client import generate_response
from rag.retriever import knowledge_base_status, retrieve


def get_knowledge_base_status():
    return knowledge_base_status()


def _build_context(results):
    sections = []

    for index, item in enumerate(results, start=1):
        metadata = item["metadata"]
        sections.append(
            f"SOURCE {index}\n"
            f"Title: {metadata['title']}\n"
            f"Publisher: {metadata['publisher']}\n"
            f"Category: {metadata['category']}\n"
            f"Content:\n{item['content']}"
        )

    return "\n\n".join(sections)


def _unique_sources(results):
    sources = []
    seen = set()

    for item in results:
        metadata = item["metadata"]
        url = metadata.get("url", "").strip()

        if not url or url in seen:
            continue

        seen.add(url)
        sources.append(
            {
                "title": metadata["title"],
                "publisher": metadata["publisher"],
                "url": url,
            }
        )

    return sources


def answer_with_rag(query: str):
    results = retrieve(query, top_k=4)

    if not results:
        return {
            "answer": (
                "I could not find relevant information in the current "
                "CareGuide knowledge base. Please try a different question."
            ),
            "sources": [],
        }

    context = _build_context(results)

    system_prompt = """
You are CareGuide AI, a healthcare information assistant.

Use only the supplied CareGuide knowledge-base context to answer.

Rules:
- Do not diagnose.
- Do not present yourself as a doctor.
- Do not invent medical facts.
- Do not claim a source supports something that is not in the supplied context.
- If the context does not answer the question, say so clearly.
- Do not make individualized prescribing or treatment decisions.
- If the supplied context indicates potentially serious symptoms, recommend
  appropriate urgent or emergency medical evaluation.
- Use clear, understandable language.
- Keep the answer concise but useful.
"""

    user_prompt = f"""
User question:
{query}

CareGuide knowledge-base context:
{context}

Answer the user's question using the supplied context.
"""

    answer = generate_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    return {
        "answer": answer,
        "sources": _unique_sources(results),
    }
