"""CareGuide AI multi-agent orchestration layer."""

from agents.router_agent import route_request
from agents.safety_agent import assess_request
from agents.language_agent import select_language
from agents.specialist_agents import run_specialist


def run_agent_workflow(query: str, rag_runner):
    """Run routing, safety, language, specialist, RAG and evidence stages."""
    route = route_request(query)
    language = select_language(query)
    safety = assess_request(query)

    if safety["needs_escalation"] and safety["block_normal_answer"]:
        return {
            "answer": safety["message"],
            "sources": [],
            "trace": {"workflow": route, "agents": ["Router Agent", "Safety Agent"]},
            "query": {"category": route, "expanded_queries": []},
            "evidence": {"verified": False, "note": "Safety escalation response."},
            "agent_trace": {
                "route": route,
                "language": language,
                "safety": safety,
                "specialist": None,
                "agents": ["Router Agent", "Safety Agent"],
            },
        }

    specialist = run_specialist(route, query)
    result = rag_runner(query, specialist_instruction=specialist["instruction"], language=language)
    result["agent_trace"] = {
        "route": route,
        "language": language,
        "safety": safety,
        "specialist": specialist,
        "agents": [
            "Router Agent",
            "Safety Agent",
            specialist["agent_name"],
            "Research Agent",
            "Evidence Agent",
            "Response Agent",
        ],
    }
    return result
