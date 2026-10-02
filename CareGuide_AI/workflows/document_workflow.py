"""Medical document understanding workflow.

The workflow explains what is present in an uploaded document. It does not
independently diagnose conditions or prescribe treatment.
"""

from agents.llm_client import generate_response
from agents.language_agent import language_instruction
from documents.processor import process_document


def run_document_workflow(document_text: str, filename: str, language: str = "english", focus: str = "") -> dict:
    processed = process_document(document_text)
    text = processed["text"]

    if not text:
        return {
            "answer": "I could not extract readable text from this document. If it is a scanned/image-only PDF, an OCR-enabled version is needed for text analysis.",
            "processed": processed,
            "trace": {"workflow": "Document Understanding Agent", "status": "no_text"},
        }

    # Keep uploaded documents bounded before sending content to the model.
    # This is a safety/cost guard, not a claim about document meaning.
    max_chars = 18000
    clipped = text[:max_chars]
    if len(text) > max_chars:
        clipped += "\n[Document text truncated for processing.]"

    language_label = "Urdu" if language == "urdu" else "English"
    focus_text = focus.strip() or "Give a plain-language overview of what the document says."

    system_prompt = f"""You are CareGuide AI's Document Understanding Agent.
Explain a user-uploaded healthcare document using ONLY the document text supplied below.
Do not diagnose a disease, interpret a result as a diagnosis, prescribe treatment, recommend changing medication, or invent missing values.
Do not assume a reference range, normal/abnormal threshold, medical history, or patient identity that is not explicitly present.
Distinguish clearly between: (1) what the document explicitly states and (2) what cannot be determined from it.
If a result, medication, or instruction is unclear, say it is unclear and suggest discussing the original document with a qualified healthcare professional.
Keep the answer concise and easy to understand. Never claim to be the user's doctor.
Answer in {language_label}. {language_instruction(language)}
"""

    user_prompt = f"""DOCUMENT FILENAME: {filename}

USER FOCUS:
{focus_text}

DOCUMENT CONTENT:
{clipped}

TASK:
Summarize the document in a few concise sections. Mention important dates, named tests/medications, and reported values only when they are explicitly present. Do not diagnose or prescribe."""

    answer = generate_response(system_prompt, user_prompt)
    return {
        "answer": answer,
        "processed": processed,
        "trace": {
            "workflow": "Document Understanding Agent",
            "status": "completed",
            "characters_processed": len(clipped),
            "truncated": len(text) > max_chars,
        },
    }
