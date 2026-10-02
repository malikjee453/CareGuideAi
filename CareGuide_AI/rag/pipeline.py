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
    """Retrieve relevant knowledge and generate a grounded answer."""
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
You are CareGuide AI, an evidence-grounded healthcare information assistant.

Your job is to answer the user's healthcare information question using ONLY the
CareGuide knowledge-base context supplied in the user message.

Rules:
- Answer the user's actual question directly. Never use a generic greeting as
  the answer when a question was provided.
- Do not diagnose a person or claim to be a doctor.
- Do not invent medical facts, statistics, treatments, or sources.
- Do not claim that information is supported by a source unless it appears in
  the supplied context.
- If the supplied context does not contain enough information to answer a
  question, say that clearly rather than filling the gap from outside knowledge.
- Do not provide personalized prescribing, dosage changes, or treatment
  decisions.
- If the context describes warning signs that require urgent evaluation,
  mention that appropriately when relevant to the question.
- Keep the answer concise but understandable.
- Prefer short paragraphs and bullet points when they improve readability.
- Do not add a separate Sources section; the application displays sources.
"""

    user_prompt = f"""
User question:
{query.strip()}

CareGuide knowledge-base context:
{context}

Now answer the user's question using the supplied context. Start directly with
useful information; do not begin with a generic greeting.
"""

    answer = generate_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    return {
        "answer": answer,
        "sources": _unique_sources(results),
    }
