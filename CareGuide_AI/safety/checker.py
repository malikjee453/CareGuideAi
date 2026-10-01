"""Safety checking scaffold."""


def check_response(text: str) -> dict:
    return {
        "safe": True,
        "needs_escalation": False,
    }
