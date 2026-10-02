"""Safety checking and response-risk controls."""

from safety.risk_engine import assess_risk


def check_response(text: str) -> dict:
    risk = assess_risk(text)
    return {
        "safe": risk.level != "emergency",
        "risk_level": risk.level,
        "needs_escalation": risk.level in {"high", "emergency"},
        "matched": list(risk.matched),
        "reason": risk.reason,
    }
