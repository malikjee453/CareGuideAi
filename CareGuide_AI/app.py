import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE
from agents.agent_manager import run_agent_workflow
from rag.pipeline import answer_with_rag, get_knowledge_base_status

st.set_page_config(page_title=APP_NAME, page_icon="🏥", layout="wide")

st.title("🏥 CareGuide AI")
st.caption(APP_TAGLINE)
st.info("CareGuide AI provides healthcare information and education. It does not diagnose conditions or replace a qualified healthcare professional.")

question = st.text_area("What would you like to know?", placeholder="Ask a healthcare information question...", height=120)

if st.button("Ask CareGuide AI", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("CareGuide AI agents are working: routing, safety check, retrieval, evidence review, and response..."):
            try:
                result = run_agent_workflow(question, answer_with_rag)
                st.markdown("### CareGuide AI")
                st.write(result["answer"])

                sources = result.get("sources", [])
                if sources:
                    st.markdown("### Sources")
                    for index, source in enumerate(sources, start=1):
                        st.markdown(f"**{index}. {source['title']}**  \nPublisher: {source['publisher']}  \n[Open source]({source['url']})")

                with st.expander("Multi-Agent workflow trace"):
                    a = result.get("agent_trace", {})
                    st.write(f"Router Agent: **{a.get('route', 'general')}**")
                    st.write(f"Language Agent: **{a.get('language', 'english')}**")
                    specialist = a.get("specialist") or {}
                    st.write(f"Specialist Agent: **{specialist.get('agent_name', 'N/A')}**")
                    safety = a.get("safety") or {}
                    st.write(f"Safety Agent: **{'escalation flagged' if safety.get('needs_escalation') else 'passed'}**")
                    st.write("Agents used: **" + " → ".join(a.get("agents", [])) + "**")

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
            except Exception:
                st.error("CareGuide AI could not process the request. Check the Streamlit logs for details.")

with st.expander("Knowledge base status"):
    status = get_knowledge_base_status()
    st.write(f"Documents found: **{status.get('documents', 0)}**")
    st.write(f"Chunks created: **{status.get('chunks', 0)}**")
    st.write(f"Retrieval: **{status.get('retrieval', 'Available')}**")
    st.write(f"Knowledge base path: `{status.get('path', '')}`")
    if status.get("documents", 0) == 0:
        st.warning("No knowledge-base documents were found. Make sure the knowledge_base folder is committed to GitHub.")
