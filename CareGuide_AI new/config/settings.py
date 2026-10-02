import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "CareGuide AI"
APP_TAGLINE = "Evidence-grounded healthcare information and navigation assistant"
MODEL_NAME = "openai/gpt-oss-120b"


def _load_groq_api_key():
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key.strip()

    try:
        import streamlit as st

        key = st.secrets.get("GROQ_API_KEY")
        if key:
            return str(key).strip()
    except Exception:
        pass

    return None


GROQ_API_KEY = _load_groq_api_key()

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured. "
        "Add it to .env locally or Streamlit Secrets when deployed."
    )
