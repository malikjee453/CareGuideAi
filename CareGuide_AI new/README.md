# CareGuide AI

CareGuide AI is an evidence-grounded healthcare information and navigation platform.

It is designed to help users understand trusted healthcare information, medical terminology, healthcare documents, medication information, and appropriate next steps.

> CareGuide AI is an information and education product, not an AI doctor and not a replacement for qualified healthcare professionals.

## Current step: Basic RAG

This version includes a clean first RAG implementation:

```text
User question
    ↓
TF-IDF retrieval over local healthcare knowledge base
    ↓
Relevant source passages
    ↓
Groq: openai/gpt-oss-120b
    ↓
Answer + source links
```

The local retrieval layer does not require a second API key.

## Stack

- Python
- Streamlit
- Groq API
- `openai/gpt-oss-120b`
- scikit-learn TF-IDF retrieval
- GitHub
- Streamlit Community Cloud

## Project structure

```text
CareGuide_AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── agents/
├── config/
├── documents/
├── evaluation/
├── knowledge_base/
├── rag/
├── safety/
├── ui/
└── workflows/
```

## Local setup

### 1. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Groq

Copy `.env.example` to `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_real_key_here
```

Never commit `.env` or expose an API key in source code.

### 4. Run

```bash
streamlit run app.py
```

## Streamlit Community Cloud

Add this to the app's Streamlit Secrets:

```toml
GROQ_API_KEY = "your_real_key_here"
```

Then deploy `app.py` from the `CareGuide_AI` folder.

## Basic RAG knowledge base

The included knowledge base contains small starter documents for:

- Hypertension
- Diabetes
- Medication safety
- Urgent health warnings

Each document stores source metadata such as title, publisher, URL, category, and update date.

## Development roadmap

1. Foundation
2. Basic RAG — current
3. Advanced RAG
4. Research agent
5. Router agent
6. Specialist agents
7. Safety agent
8. EvidenceGuard
9. English/Urdu language workflow
10. Healthcare document workflow
11. Evaluation
12. Production deployment

## Safety

The system should not diagnose users, fabricate medical information, or represent itself as a healthcare professional. Higher-risk use cases require appropriate safeguards, source verification, and escalation to qualified professionals.
