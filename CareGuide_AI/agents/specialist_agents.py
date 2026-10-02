"""Specialist-agent selection used by the Agent Manager."""

SPECIALISTS = {
    "healthcare": ("Medical Information Agent", "Focus on general healthcare information, definitions, symptoms, risk factors, prevention, and when professional care may be appropriate."),
    "medication": ("Medication Information Agent", "Focus on medication purpose, general safety information, common cautions, and source-grounded information. Do not prescribe or invent doses."),
    "document": ("Document Understanding Agent", "Focus on explaining medical-document terminology and reported information without diagnosing the person."),
    "safety": ("Safety Agent", "Prioritize urgent-care guidance and safe escalation."),
}

def run_specialist(route: str, query: str) -> dict:
    name, instruction = SPECIALISTS.get(route, SPECIALISTS["healthcare"])
    return {"agent_name": name, "route": route, "instruction": instruction}
