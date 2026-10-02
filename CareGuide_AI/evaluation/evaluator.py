"""Evaluation scaffold for retrieval, generation, evidence and safety."""


def evaluate_response(question: str, answer: str) -> dict:
    return {
        "question": question,
        "answer": answer,
        "metrics": {},
    }
