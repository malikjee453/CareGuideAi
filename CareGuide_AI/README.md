# CareGuide AI — Step 3 Advanced RAG

CareGuide AI is an evidence-grounded healthcare information and navigation assistant.
It is educational and does not diagnose conditions or replace qualified healthcare professionals.

## Step 3 architecture

User question → query understanding → deterministic query expansion → hybrid retrieval → metadata preference → reranking → context compression → GPT-OSS-120B grounded response → evidence/provenance check → sources.

The retrieval layer remains local and does not require a second API key.

## Streamlit

Main module:

`CareGuide_AI/app.py`

Required secret:

`GROQ_API_KEY`

Model:

`openai/gpt-oss-120b`


## Step 7 — English + Urdu Language Agent
- User-selectable English or Urdu output.
- Automatic Urdu detection from Urdu script or explicit Urdu requests.
- Urdu responses are rendered right-to-left in the Streamlit UI.
- Safety escalation messages support Urdu.
- Medical answers remain grounded in the existing RAG and EvidenceGuard workflow.
