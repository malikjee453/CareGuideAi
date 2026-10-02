"""Medication workflow entry point."""

def run_medication_workflow(query: str):
    return {"workflow": "medication", "query": query, "specialist_agent": "Medication Information Agent"}
