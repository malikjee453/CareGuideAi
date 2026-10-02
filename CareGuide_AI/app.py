import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE
from rag.pipeline import answer_with_rag, get_knowledge_base_status

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
        with st.spinner("Searching the CareGuide knowledge base..."):
            try:
                result = answer_with_rag(question)

                st.markdown("### CareGuide AI")
                st.write(result["answer"])

                sources = result.get("sources", [])

                if sources:
                    st.markdown("### Sources")
                    for index, source in enumerate(sources, start=1):
                        st.markdown(
                            f"**{index}. {source['title']}**  \n"
                            f"Publisher: {source['publisher']}  \n"
                            f"[Open source]({source['url']})"
                        )

            except Exception as exc:
                st.error("CareGuide AI could not process the request.")
                st.exception(exc)

with st.expander("Knowledge base status"):
    status = get_knowledge_base_status()
    st.write(f"Documents found: **{status['documents']}**")
    st.write(f"Chunks created: **{status['chunks']}**")
    st.write(f"Knowledge base path: `{status['path']}`")

    if status["documents"] == 0:
        st.warning(
            "No knowledge-base documents were found. "
            "Make sure the knowledge_base folder and its .md files are committed to GitHub."
        )
