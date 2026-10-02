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


def _is_generic_greeting(answer: str) -> bool:
    """Detect responses that do not answer the user's question."""
    if not answer or not answer.strip():
        return True

    text = " ".join(answer.strip().split()).lower()
    generic = {
        "hello!",
        "hello",
        "hi!",
        "hi",
        "hey!",
        "hey",
        "hello! 👋",
        "hello 👋",
        "hi! 👋",
        "hi 👋",
        "hey! 👋",
        "hey 👋",
        "hello! how can i assist you today?",
        "hello, how can i assist you today?",
        "how can i assist you today?",
    }
    return text in generic


def _context_fallback(results):
    """Create a safe answer from retrieved text if the model gives no useful answer."""
    paragraphs = []
    for item in results:
        for paragraph in item["content"].split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph and paragraph not in paragraphs:
                paragraphs.append(paragraph)

    # Keep the fallback concise while preserving source wording and meaning.
    useful = paragraphs[:3]
    if not useful:
        return "I found a relevant source, but I could not generate an answer from it."

    return "Based on the CareGuide knowledge base:\n\n" + "\n\n".join(useful)


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

Answer the user's ACTUAL question using ONLY the CareGuide knowledge-base
context supplied below.

STRICT REQUIREMENTS:
- You MUST answer the user's question.
- NEVER answer with only a greeting such as "Hello", "Hi", or "How can I help?".
- Start with the useful healthcare information requested by the user.
- Do not diagnose a person or claim to be a doctor.
- Do not invent medical facts, statistics, treatments, dosages, or sources.
- If the supplied context is insufficient, explicitly say what is not covered.
- Do not provide personalized prescribing, dosage changes, or treatment decisions.
- Mention relevant warning signs from the context when appropriate.
- Keep the response concise and easy to understand.
- Do not add a Sources section because the application displays sources separately.
"""

    user_prompt = f"""
USER QUESTION:
{query.strip()}

CAREGUIDE KNOWLEDGE-BASE CONTEXT:
{context}

TASK:
Answer the USER QUESTION directly and concisely using only the supplied context.
Your first sentence must contain useful information answering the question.
"""

    answer = generate_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    # A small number of hosted/model responses can ignore the requested task and
    # return a greeting. Retry once with an even stricter instruction, then use
    # an extractive source-grounded fallback rather than showing a useless reply.
    if _is_generic_greeting(answer):
        retry_prompt = f"""
Answer this healthcare information question now:

{query.strip()}

Use only this retrieved CareGuide source material:

{context}

Return 2-4 concise sentences that directly answer the question.
Do NOT greet the user. Do NOT say hello. Do NOT ask how you can help.
If the source does not contain enough information, say that explicitly.
"""
        retry = generate_response(
            system_prompt=system_prompt,
            user_prompt=retry_prompt,
        )
        answer = retry if not _is_generic_greeting(retry) else _context_fallback(results)

    return {
        "answer": answer,
        "sources": _unique_sources(results),
    }

