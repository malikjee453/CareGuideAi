"""CareGuide AI multi-agent orchestration layer."""

from agents.router_agent import route_request
from agents.safety_agent import assess_request
from agents.language_agent import select_language
from agents.specialist_agents import run_specialist
from safety.rules import EMERGENCY_MESSAGE, HIGH_RISK_MESSAGE

def _safety_message(language: str, level: str) -> str:
    if language == "urdu":
        if level == "emergency":
            return (
                "یہ پیغام ایک ہنگامی صورتحال کی نشاندہی کر سکتا ہے۔ براہِ کرم فوراً طبی مدد حاصل کریں "
                "یا اپنے مقامی ایمرجنسی سروس سے رابطہ کریں۔ ایسی صورتحال میں صرف AI کے جواب پر انحصار نہ کریں۔"
            )
        if level == "high":
            return (
                "یہ علامات فوری طبی معائنے کی ضرورت ظاہر کر سکتی ہیں۔ CareGuide AI عمومی معلومات دے سکتا ہے، "
                "لیکن ہنگامی علامات کو گھر پر سنبھالنے کا فیصلہ کرنے کے لیے اس پر انحصار نہ کریں۔"
            )
    return EMERGENCY_MESSAGE if level == "emergency" else HIGH_RISK_MESSAGE

def run_agent_workflow(query: str, rag_runner, requested_language: str | None = None):
    route = route_request(query)
    language = select_language(query, requested_language)
    safety = assess_request(query)

    if safety["needs_escalation"] and safety["block_normal_answer"]:
        return {
            "answer": _safety_message(language, "emergency"),
            "sources": [],
            "trace": {"workflow": route, "agents": ["Router Agent", "Safety Agent"]},
            "query": {"category": route, "expanded_queries": []},
            "evidence": {"verified": False, "note": "Safety escalation response."},
            "agent_trace": {
                "route": route, "language": language, "safety": safety, "specialist": None,
                "agents": ["Router Agent", "Safety Agent"],
            },
        }

    specialist = run_specialist(route, query)
    result = rag_runner(query, specialist_instruction=specialist["instruction"], language=language)
    result["agent_trace"] = {
        "route": route, "language": language, "safety": safety, "specialist": specialist,
        "agents": ["Router Agent", "Safety Agent", specialist["agent_name"], "Research Agent", "Evidence Agent", "Response Agent"],
    }
    return result
