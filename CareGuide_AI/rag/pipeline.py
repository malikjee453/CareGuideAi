from agents.llm_client import generate_response
from rag.retriever import retrieve


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
        url = metadata.get("url", "")

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
                "CareGuide knowledge base. Please try a different question "
                "or consult a qualified healthcare professional."
            ),
            "sources": [],
        }

    context = _build_context(results)

    system_prompt = """
You are CareGuide AI, a healthcare information assistant.

Answer using ONLY the supplied knowledge-base context.

Important rules:
- Do not diagnose the user.
- Do not present yourself as a doctor.
- Do not invent facts that are not supported by the context.
- If the context does not answer the question, say so.
- Do not give personalized treatment instructions.
- For potentially urgent symptoms or situations, advise appropriate urgent
  or emergency medical evaluation.
- Explain medical information in clear, understandable language.
- Keep the answer reasonably concise.
- Do not create fake citations or sources.
"""

    user_prompt = f"""
User question:
{query}

Knowledge-base context:
{context}

Write a clear educational answer based on the context above.
"""

    answer = generate_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    return {
        "answer": answer,
        "sources": _unique_sources(results),
    }
