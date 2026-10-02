"""Route user requests to the appropriate specialist workflow."""


def route_request(user_query: str) -> str:
    text = user_query.lower()
    if any(word in text for word in ["medicine", "medication", "drug", "tablet", "dose", "pill", "side effect"]):
        return "medication"
    if any(word in text for word in ["document", "report", "lab result", "prescription", "medical report"]):
        return "document"
    if any(word in text for word in ["emergency", "urgent", "chest pain", "can't breathe", "cannot breathe", "unconscious"]):
        return "safety"
    return "healthcare"
