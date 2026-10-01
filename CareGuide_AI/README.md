# CareGuide AI

CareGuide AI is an evidence-grounded healthcare information and navigation platform.

It is designed to help users understand trusted healthcare information, medical terminology, healthcare documents, medication information, and appropriate next steps.

> CareGuide AI is an information and education product, not an AI doctor and not a replacement for qualified healthcare professionals.

## Current stack

- Python
- Streamlit
- Groq API
- `openai/gpt-oss-120b`
- GitHub for source control
- Streamlit Community Cloud for deployment

## Project architecture

```text
User
  ↓
Streamlit UI
  ↓
Workflow Layer
  ↓
Agent Layer
  ├── Router Agent
  ├── Research Agent
  ├── Medical Information Agent
  ├── Medication Information Agent
  ├── Safety Agent
  ├── Evidence Verification Agent
  ├── Language Agent
  └── Response Agent
  ↓
RAG / Knowledge Base
  ↓
Verified Response + Sources
```

The current starter application uses the Groq LLM directly. RAG, evidence verification, specialist agents, document processing, and advanced workflows are scaffolded for the next development stages.

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

Never commit `.env` to GitHub.

### 4. Run

```bash
streamlit run app.py
```

## Streamlit Community Cloud

1. Push this project to GitHub.
2. Open Streamlit Community Cloud.
3. Select the GitHub repository and `app.py`.
4. Add the secret:

```toml
GROQ_API_KEY = "your_real_key_here"
```

5. Deploy.

## Development roadmap

1. Foundation
2. Knowledge base ingestion
3. Basic RAG
4. Advanced RAG
5. Research agent
6. Router agent
7. Specialist agents
8. Safety agent
9. EvidenceGuard
10. English/Urdu language workflow
11. Healthcare document workflow
12. Evaluation
13. Production deployment

## Safety

The system should not diagnose users, fabricate medical information, or represent itself as a healthcare professional. Higher-risk use cases require appropriate safeguards, source verification, and escalation to qualified professionals.
