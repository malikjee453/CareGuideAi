import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE
from rag.pipeline import answer_with_rag, get_knowledge_base_status

st.set_page_config(page_title=APP_NAME, page_icon="🏥", layout="wide")

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
        with st.spinner("Understanding your question and searching trusted evidence..."):
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

                with st.expander("Advanced RAG trace"):
                    q = result.get("query", {})
                    t = result.get("trace", {})
                    e = result.get("evidence", {})
                    st.write(f"Query category: **{q.get('category') or 'general'}**")
                    st.write(f"Expanded queries: **{len(q.get('expanded_queries', []))}**")
                    st.write(f"Retrieved candidates: **{t.get('candidate_count', 0)}**")
                    st.write(f"After reranking: **{t.get('reranked_count', 0)}**")
                    st.write(f"After context compression: **{t.get('compressed_count', 0)}**")
                    st.write(f"Evidence check: **{'supported' if e.get('verified') else 'needs caution'}**")

            except Exception as exc:
                st.error("CareGuide AI could not process the request.")
                st.exception(exc)

with st.expander("Knowledge base status"):
    status = get_knowledge_base_status()
    st.write(f"Documents found: **{status['documents']}**")
    st.write(f"Chunks created: **{status['chunks']}**")
    st.write(f"Retrieval: **{status['retrieval']}**")
    st.write(f"Knowledge base path: `{status['path']}`")
    if status["documents"] == 0:
        st.warning("No knowledge-base documents were found. Make sure the knowledge_base folder is committed to GitHub.")
