"""Safety agent for risk-aware routing before normal generation."""

from safety.risk_engine import assess_risk
from safety.rules import EMERGENCY_MESSAGE, HIGH_RISK_MESSAGE


def assess_request(text: str) -> dict:
    risk = assess_risk(text)

    if risk.level == "emergency":
        message = EMERGENCY_MESSAGE
        block_normal_answer = True
    elif risk.level == "high":
        message = HIGH_RISK_MESSAGE
        block_normal_answer = False
    else:
        message = ""
        block_normal_answer = False

    return {
        "safe": risk.level != "emergency",
        "risk_level": risk.level,
        "needs_escalation": risk.level in {"high", "emergency"},
        "block_normal_answer": block_normal_answer,
        "matched": list(risk.matched),
        "reason": risk.reason,
        "recommended_action": risk.recommended_action,
        "message": message,
    }


def safety_check(text: str) -> dict:
    result = assess_request(text)
    return {
        "safe": result["safe"],
        "risk_level": result["risk_level"],
        "needs_escalation": result["needs_escalation"],
        "reason": result["reason"],
    }
