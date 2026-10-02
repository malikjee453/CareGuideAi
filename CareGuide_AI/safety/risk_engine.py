"""Rule-based healthcare risk triage for routing and response safety.

This layer is intentionally conservative and does not diagnose conditions.
It only identifies phrases that may warrant a safer response or escalation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskResult:
    level: str
    matched: tuple[str, ...]
    reason: str
    recommended_action: str


EMERGENCY_PATTERNS = (
    "severe chest pain",
    "chest pain and difficulty breathing",
    "can't breathe",
    "cannot breathe",
    "severe difficulty breathing",
    "not breathing",
    "unconscious",
    "not responding",
    "severe bleeding",
    "stroke symptoms",
    "signs of stroke",
    "suicide",
    "kill myself",
    "trying to kill myself",
    "overdose",
    "poisoning",
)

HIGH_RISK_PATTERNS = (
    "difficulty breathing",
    "shortness of breath",
    "fainting",
    "passed out",
    "seizure",
    "heavy bleeding",
    "severe allergic reaction",
    "swelling of the throat",
    "vomiting blood",
    "coughing blood",
    "blood in vomit",
    "blood in stool",
)

MODERATE_RISK_PATTERNS = (
    "severe pain",
    "persistent vomiting",
    "high fever",
    "worsening symptoms",
    "getting worse",
    "new confusion",
    "confusion",
    "severe headache",
    "vision changes",
)


def _matches(text: str, patterns: tuple[str, ...]) -> list[str]:
    normalized = " ".join(text.lower().split())
    return [pattern for pattern in patterns if pattern in normalized]


def assess_risk(text: str) -> RiskResult:
    """Classify request risk without attempting diagnosis."""
    emergency = _matches(text, EMERGENCY_PATTERNS)
    if emergency:
        return RiskResult(
            level="emergency",
            matched=tuple(emergency),
            reason="The message contains language associated with a potentially time-critical situation.",
            recommended_action="Seek immediate emergency medical help rather than relying on an AI response.",
        )

    high = _matches(text, HIGH_RISK_PATTERNS)
    if high:
        return RiskResult(
            level="high",
            matched=tuple(high),
            reason="The message contains symptoms that may require prompt professional assessment.",
            recommended_action="Seek prompt medical assessment, especially if symptoms are severe, sudden, or worsening.",
        )

    moderate = _matches(text, MODERATE_RISK_PATTERNS)
    if moderate:
        return RiskResult(
            level="moderate",
            matched=tuple(moderate),
            reason="The message contains symptoms that may need additional clinical context.",
            recommended_action="Consider contacting a qualified healthcare professional for appropriate assessment.",
        )

    return RiskResult(
        level="low",
        matched=(),
        reason="No configured high-risk phrase was detected.",
        recommended_action="Normal evidence-grounded information workflow may continue.",
    )
