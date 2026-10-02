"""Language agent for English/Urdu request detection."""

URDU_MARKERS = ["urdu", "اردو", "جواب اردو", "اردو میں", "in urdu"]

def select_language(user_request: str) -> str:
    text = user_request.lower()
    return "urdu" if any(marker in text for marker in URDU_MARKERS) else "english"

def language_instruction(language: str) -> str:
    if language == "urdu":
        return "Answer in clear Urdu. Do not switch to Hindi. Keep medical terms understandable and preserve important English medical terms in parentheses when useful."
    return "Answer in clear, concise English."

def translate_response(text: str, language: str) -> str:
    return text
