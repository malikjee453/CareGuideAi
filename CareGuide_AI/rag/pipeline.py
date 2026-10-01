from agents.llm_client import generate_response
from rag.retriever import retrieve, knowledge_base_status


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

Use ONLY the supplied CareGuide knowledge-base context.

Rules:
- Do not diagnose.
- Do not present yourself as a doctor.
- Do not invent medical facts.
- Do not claim information is supported by a source unless it appears in the context.
- If the context does not answer the question, clearly say that.
- Do not provide personalized prescribing or treatment decisions.
- If the question describes potentially serious symptoms, recommend appropriate
  urgent or emergency medical evaluation.
- Use clear, understandable language.
- Keep the answer concise but useful.
"""

    user_prompt = f"""
User question:
{query}

CareGuide knowledge-base context:
{context}

Answer the user's question using the context above.
"""

    answer = generate_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    return {
        "answer": answer,
        "sources": _unique_sources(results),
    }
