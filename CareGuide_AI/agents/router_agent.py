"""Route user requests to the appropriate CareGuide workflow."""


def route_request(user_query: str) -> str:
    text = user_query.lower()

    if any(word in text for word in ["medicine", "medication", "drug", "tablet", "dose"]):
        return "medication"

    if any(word in text for word in ["document", "report", "lab result", "prescription"]):
        return "document"

    return "healthcare"
