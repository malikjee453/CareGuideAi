import re

# Small, deterministic healthcare query expansion. It improves recall without
# requiring another API call or another model.
EXPANSIONS = {
    "hypertension": ["high blood pressure", "blood pressure"],
    "high blood pressure": ["hypertension", "blood pressure"],
    "diabetes": ["blood glucose", "insulin", "type 2 diabetes"],
    "medicine": ["medication", "drug", "prescribed medicine"],
    "medicines": ["medication", "drug", "prescribed medicine"],
    "medication": ["medicine", "drug", "prescribed medicine"],
    "side effects": ["adverse reaction", "reaction", "safety"],
    "symptoms": ["warning signs", "signs"],
    "emergency": ["urgent", "immediate medical care", "rapidly worsening"],
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", text.lower())).strip()


def detect_category(query: str) -> str | None:
    text = normalize(query)
    if any(term in text for term in ["medicine", "medication", "drug", "tablet", "dose", "side effect"]):
        return "medications"
    if any(term in text for term in ["emergency", "urgent", "chest pain", "difficulty breathing", "fainting", "severe"]):
        return "emergency"
    if any(term in text for term in ["diabetes", "blood sugar", "glucose", "insulin"]):
        return "public_health"
    if any(term in text for term in ["hypertension", "high blood pressure", "blood pressure"]):
        return "medical_information"
    return None


def expand_query(query: str) -> list[str]:
    base = normalize(query)
    variants = [query.strip()]

    for trigger, additions in EXPANSIONS.items():
        if trigger in base:
            for addition in additions:
                candidate = f"{query.strip()} {addition}"
                if candidate not in variants:
                    variants.append(candidate)

    return variants[:5]


def understand_query(query: str) -> dict:
    category = detect_category(query)
    return {
        "original": query.strip(),
        "normalized": normalize(query),
        "category": category,
        "expanded_queries": expand_query(query),
    }
