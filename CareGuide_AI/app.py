import html

import streamlit as st

from config.settings import APP_NAME, APP_TAGLINE
from agents.agent_manager import run_agent_workflow
from rag.pipeline import answer_with_rag, get_knowledge_base_status
from documents.extractor import extract_text_from_bytes
from workflows.document_workflow import run_document_workflow

st.set_page_config(page_title=APP_NAME, page_icon="🏥", layout="wide")

st.markdown(
    """
    <div class="cg-brand">
        <span class="cg-icon">🏥</span>
        <span class="cg-name">CareGuide</span><span class="cg-ai">AI</span>
    </div>
    <style>
        .cg-brand {
            display: flex;
            align-items: baseline;
            gap: 0.22rem;
            margin: 0.15rem 0 0.15rem 0;
            line-height: 1;
        }
        .cg-icon {
            font-size: 2.7rem;
            margin-right: 0.12rem;
        }
        .cg-name {
    font-size: 3.2rem;
    font-weight: 950;
    letter-spacing: -0.045em;
    color: #173B5E;
}

.cg-ai {
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.10em;
    color: #D28B35;
    vertical-align: super;
    position: relative;
    top: -0.85rem;
    margin-left: 0.08rem;
}
    </style>
    """,
    unsafe_allow_html=True,
)
st.caption(APP_TAGLINE)
st.info("CareGuide AI provides healthcare information and education. It does not diagnose conditions or replace a qualified healthcare professional.")

st.subheader("Healthcare Q&A")
question = st.text_area("What would you like to know?", placeholder="Ask a healthcare information question...", height=120)
requested_language = st.radio("Answer language", ["English", "Urdu"], horizontal=True, help="Choose the language for the answer. Urdu uses Urdu script, not Hindi.")
language_code = "urdu" if requested_language == "Urdu" else "english"

if st.button("Ask CareGuide AI", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("CareGuide AI agents are working: language, routing, safety, retrieval, evidence review, and response..."):
            try:
                result = run_agent_workflow(question, answer_with_rag, requested_language=language_code)
                answer = result.get("answer", "")
                st.markdown("### CareGuide AI")
                if result.get("agent_trace", {}).get("language") == "urdu":
                    safe_answer = html.escape(answer).replace("\n", "<br>")
                    st.markdown(f'<div dir="rtl" style="text-align:right; font-size:1.08rem; line-height:2.0;">{safe_answer}</div>', unsafe_allow_html=True)
                else:
                    st.write(answer)

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
                    risk_level = safety.get("risk_level", "low")
                    st.write(f"Safety Agent: **{risk_level.replace('_', ' ').title()} risk**")
                    if safety.get("matched"):
                        st.write("Matched safety signals: **" + ", ".join(safety.get("matched", [])) + "**")
                    if safety.get("recommended_action"):
                        st.caption(safety.get("recommended_action"))
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
                    st.write(f"EvidenceGuard: **{'verified' if e.get('verified') else 'needs review'}**")
                    claims = e.get("claims", [])
                    if claims:
                        st.write(f"Claims checked: **{len(claims)}**")
                        for claim in claims:
                            marker = "✓" if claim.get("supported") else "⚠"
                            st.write(f"{marker} {claim.get('support_score', 0):.0%} support — {claim.get('source', 'No matching source')}")
                    if e.get("unsupported_claims"):
                        st.caption("EvidenceGuard requested a revision for weakly supported claims.")
            except Exception as exc:
                st.error("CareGuide AI could not process the request. Please try again.")
                with st.expander("Technical details"):
                    st.code(type(exc).__name__ + ": " + str(exc)[:500])

st.divider()
st.subheader("📄 Medical Document Understanding")
st.caption("Upload a healthcare document and CareGuide AI will explain what the document explicitly says. It will not diagnose conditions or prescribe treatment.")

uploaded_document = st.file_uploader(
    "Upload a medical document",
    type=["pdf", "docx", "txt", "md", "csv"],
    help="Supported: text-based PDF, DOCX, TXT, MD, and CSV. Scanned/image-only PDFs may require OCR and may not contain extractable text.",
)
document_focus = st.text_input(
    "Optional: what would you like explained?",
    placeholder="Example: Explain the test results in simple language.",
)

if st.button("Analyze Medical Document", type="secondary"):
    if uploaded_document is None:
        st.warning("Please upload a document first.")
    else:
        with st.spinner("Extracting and analyzing the document safely..."):
            try:
                file_bytes = uploaded_document.getvalue()
                extracted_text = extract_text_from_bytes(file_bytes, uploaded_document.name)
                result = run_document_workflow(
                    extracted_text,
                    uploaded_document.name,
                    language=language_code,
                    focus=document_focus,
                )

                st.markdown("### Document Explanation")
                if language_code == "urdu":
                    safe_answer = html.escape(result.get("answer", "")).replace("\n", "<br>")
                    st.markdown(f'<div dir="rtl" style="text-align:right; font-size:1.08rem; line-height:2.0;">{safe_answer}</div>', unsafe_allow_html=True)
                else:
                    st.write(result.get("answer", ""))

                processed = result.get("processed", {})
                st.markdown("### Document Details")
                st.write(f"File: **{uploaded_document.name}**")
                st.write(f"Extracted words: **{processed.get('word_count', 0)}**")
                if processed.get("sections"):
                    st.write("Detected sections/headings: **" + ", ".join(processed["sections"][:15]) + "**")
                if processed.get("possible_measurement_lines"):
                    with st.expander("Detected measurement lines — not medically interpreted"):
                        for line in processed["possible_measurement_lines"]:
                            st.write("- " + line)

                with st.expander("Document workflow trace"):
                    trace = result.get("trace", {})
                    st.write(f"Workflow: **{trace.get('workflow', 'Document Understanding Agent')}**")
                    st.write(f"Status: **{trace.get('status', 'unknown')}**")
                    st.write(f"Characters processed: **{trace.get('characters_processed', 0)}**")
                    if trace.get("truncated"):
                        st.caption("The document was longer than the processing limit, so only the beginning was analyzed.")
                    st.caption("CareGuide AI reports document content; it does not independently diagnose or prescribe from the document.")
            except Exception as exc:
                st.error("CareGuide AI could not analyze this document. Please try again with a supported, text-readable file.")
                with st.expander("Technical details"):
                    st.code(type(exc).__name__ + ": " + str(exc)[:500])

with st.expander("Knowledge base status"):
    status = get_knowledge_base_status()
    st.write(f"Documents found: **{status.get('documents', 0)}**")
    st.write(f"Chunks created: **{status.get('chunks', 0)}**")
    st.write(f"Retrieval: **{status.get('retrieval', 'Available')}**")
    st.write(f"Knowledge base path: `{status.get('path', '')}`")
    if status.get("documents", 0) == 0:
        st.warning("No knowledge-base documents were found. Make sure the knowledge_base folder is committed to GitHub.")
