"""Safety agent for urgent-risk detection before normal generation."""

URGENT_PATTERNS = [
    "chest pain", "severe difficulty breathing", "can't breathe", "cannot breathe",
    "unconscious", "not responding", "severe bleeding", "stroke symptoms",
    "suicide", "kill myself", "overdose", "poisoning",
]

def assess_request(text: str) -> dict:
    normalized = " ".join(text.lower().split())
    matches = [p for p in URGENT_PATTERNS if p in normalized]
    if matches:
        return {
            "safe": True,
            "needs_escalation": True,
            "block_normal_answer": True,
            "matched": matches,
            "message": (
                "This may be an urgent situation. Please contact your local emergency service "
                "or seek immediate medical care rather than relying on an AI response. "
                "If someone is unconscious, having severe trouble breathing, has severe chest pain, "
                "or may have taken an overdose, get emergency help now."
            ),
        }
    return {"safe": True, "needs_escalation": False, "block_normal_answer": False, "matched": [], "message": ""}

def safety_check(text: str) -> dict:
    result = assess_request(text)
    return {"safe": result["safe"], "needs_escalation": result["needs_escalation"], "reason": result["message"]}
