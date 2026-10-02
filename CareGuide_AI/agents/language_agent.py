"""English/Urdu language routing for CareGuide AI."""

URDU_MARKERS = ("urdu", "اردو", "جواب اردو", "اردو میں", "in urdu", "in the urdu language")
URDU_SCRIPT_RANGE = tuple(chr(i) for i in range(0x0600, 0x0700))

def contains_urdu_script(text: str) -> bool:
    return any(ch in text for ch in URDU_SCRIPT_RANGE)

def select_language(user_request: str, requested_language: str | None = None) -> str:
    if requested_language in {"english", "urdu"}:
        return requested_language
    text = user_request.lower()
    if contains_urdu_script(user_request) or any(marker in text for marker in URDU_MARKERS):
        return "urdu"
    return "english"

def language_instruction(language: str) -> str:
    if language == "urdu":
        return (
            "Answer in clear, natural Urdu using Urdu script. Do not switch to Hindi. "
            "Preserve important English medical terms in parentheses when useful. "
            "Keep the answer concise and easy for a general reader to understand."
        )
    return "Answer in clear, concise English."

def render_language(text: str, language: str) -> str:
    return text
