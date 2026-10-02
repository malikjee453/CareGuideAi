"""Final response assembly placeholder."""


def build_response(answer: str, sources: list | None = None) -> dict:
    return {
        "answer": answer,
        "sources": sources or [],
    }
