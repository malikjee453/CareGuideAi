# CareGuide AI — Step 2: Basic RAG

CareGuide AI is an evidence-grounded healthcare information and navigation assistant.
This version adds a local knowledge base and basic retrieval-augmented generation (RAG).

## Model

- Groq: `openai/gpt-oss-120b`

## Project structure

```text
CareGuide_AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── agents/
├── config/
├── rag/
├── knowledge_base/
├── safety/
├── documents/
├── workflows/
├── evaluation/
└── ui/
```

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` in the same folder as `app.py`:

```env
GROQ_API_KEY=your_actual_groq_key
```

4. Start Streamlit:

```bash
streamlit run app.py
```

## Streamlit Community Cloud

Set the app's main file to:

```text
CareGuide_AI/app.py
```

Add this to Streamlit Secrets:

```toml
GROQ_API_KEY = "your_actual_groq_key"
```

Do not commit `.env` or API keys to GitHub.

## Step 2 RAG flow

```text
User question
    ↓
Local knowledge base
    ↓
Chunking + TF-IDF retrieval
    ↓
Relevant healthcare passages
    ↓
Groq GPT-OSS-120B
    ↓
Answer + sources
```

This is the basic RAG foundation. Hybrid retrieval, semantic embeddings, reranking,
EvidenceGuard, and multi-agent orchestration can be added in later steps.
