from agents.evidence_agent import verify_claims
from agents.llm_client import generate_response
from agents.language_agent import language_instruction
from rag.query import understand_query
from rag.retriever import retrieve_with_trace, knowledge_base_status


def get_knowledge_base_status():
    return knowledge_base_status()


def _build_context(results):
    sections = []
    for index, item in enumerate(results, start=1):
        metadata = item["metadata"]
        sections.append(
            f"SOURCE {index}\nTitle: {metadata['title']}\nPublisher: {metadata['publisher']}\nCategory: {metadata['category']}\nContent: {item['content']}"
        )
    return "\n\n".join(sections)


def _unique_sources(results):
    sources, seen = [], set()
    for item in results:
        metadata = item["metadata"]
        url = metadata.get("url", "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        sources.append({"title": metadata["title"], "publisher": metadata["publisher"], "url": url, "category": metadata.get("category", "general"), "content": item.get("content", "")})
    return sources


def _is_generic_greeting(answer: str) -> bool:
    if not answer or not answer.strip(): return True
    text = " ".join(answer.strip().split()).lower()
    return text in {"hello", "hello!", "hi", "hi!", "hey", "hey!", "hello! 👋", "hi! 👋", "hey! 👋", "hello! how can i assist you today?", "how can i assist you today?"}


def _context_fallback(results):
    paragraphs = []
    for item in results:
        for paragraph in item["content"].split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph and paragraph not in paragraphs: paragraphs.append(paragraph)
    return "Based on the CareGuide knowledge base:\n\n" + "\n\n".join(paragraphs[:3])


def answer_with_rag(query: str, specialist_instruction: str = "", language: str = "english"):
    understanding = understand_query(query)
    results, trace = retrieve_with_trace(query, top_k=4)
    if not results:
        return {"answer": "I could not find relevant information in the current CareGuide knowledge base. Please try a different question.", "sources": [], "trace": trace, "query": understanding, "evidence": {"verified": False, "note": "No evidence retrieved."}}

    context = _build_context(results)
    system_prompt = f"""You are CareGuide AI's Response Agent in a multi-agent healthcare information workflow.
Use ONLY the supplied CareGuide knowledge-base context. Answer the user's actual question directly and concisely. Never greet instead of answering. Do not diagnose, prescribe, invent facts, dosages, statistics, or sources. Do not make personalized treatment decisions. If context is insufficient, say so. Do not add a Sources section; the application displays sources separately.
Specialist guidance: {specialist_instruction}
Language guidance: {language_instruction(language)}
"""
    user_prompt = f"""USER QUESTION:
{query.strip()}

QUERY CATEGORY: {understanding['category'] or 'general'}

EVIDENCE:
{context}

TASK: Give a concise, evidence-grounded answer using only the evidence above."""
    answer = generate_response(system_prompt, user_prompt)
    if _is_generic_greeting(answer):
        retry = generate_response(system_prompt, f"Answer this now in 2-4 sentences. Do not greet.\nQuestion: {query}\nEvidence:\n{context}")
        answer = retry if not _is_generic_greeting(retry) else _context_fallback(results)
    sources = _unique_sources(results)
    evidence = verify_claims(answer, sources)

    # EvidenceGuard gets a second pass when substantive claims are weakly
    # supported. The revision is still restricted to the retrieved context.
    if evidence.get("unsupported_claims"):
        revision_prompt = f"""Revise the answer below so every substantive statement is directly supported by the supplied evidence.
Remove unsupported claims rather than guessing. Keep it concise (2-5 sentences), answer the user's question directly, and do not greet.

USER QUESTION:
{query.strip()}

CURRENT ANSWER:
{answer}

FLAGGED CLAIMS:
{chr(10).join('- ' + c for c in evidence['unsupported_claims'])}

EVIDENCE:
{context}
"""
        revised = generate_response(system_prompt, revision_prompt)
        revised_evidence = verify_claims(revised, sources)
        if revised and not _is_generic_greeting(revised):
            answer = revised
            evidence = revised_evidence

    return {
        "answer": answer,
        "sources": sources,
        "trace": trace,
        "query": understanding,
        "evidence": evidence,
    }
