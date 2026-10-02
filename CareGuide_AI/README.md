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
