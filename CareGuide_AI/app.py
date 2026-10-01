import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE
from agents.llm_client import generate_response

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 CareGuide AI")
st.caption(APP_TAGLINE)

st.info(
    "CareGuide AI provides healthcare information and education. "
    "It does not diagnose conditions or replace a qualified healthcare professional."
)

question = st.text_area(
    "What would you like to know?",
    placeholder="Ask a healthcare information question...",
    height=120,
)

if st.button("Ask CareGuide AI", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("CareGuide AI is thinking..."):
            system_prompt = """
You are CareGuide AI, a healthcare information assistant.

Your role is to provide clear, cautious, educational healthcare information.

Rules:
- Do not diagnose the user.
- Do not present yourself as a doctor.
- Do not invent medical facts.
- Do not claim certainty when information is uncertain.
- Encourage appropriate professional medical evaluation when needed.
- For potentially urgent situations, advise the user to seek appropriate urgent/emergency care.
- Keep answers understandable and reasonably concise.
- This initial version does not yet have a verified medical knowledge base, so do not pretend that an answer is evidence-grounded or cite sources that were not actually retrieved.
"""

            try:
                answer = generate_response(
                    system_prompt=system_prompt,
                    user_prompt=question,
                )

                st.markdown("### CareGuide AI")
                st.write(answer)

            except Exception as exc:
                st.error("CareGuide AI could not process the request.")
                st.caption(str(exc))
