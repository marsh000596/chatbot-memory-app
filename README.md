# chatbot-memory-app
A Chatbot with Memory that can work for any domain (customer service, healthcare, finance, etc.), has an advanced web-based GUI, memory storage, an API backend, and optional data-based responses.


# Chatbot with Persistent Memory

A full-stack demo: FastAPI backend, SQLite persistent memory, domain Q&A, and a web GUI.

## Features
- Persistent conversations & memory (SQLite)
- Domain-specific knowledge base (DomainQA)
- Optional semantic search over domain Q/A
- LLM integration (OpenAI by default; fallback to HF/local)
- Simple web frontend (vanilla HTML/CSS/JS)
- Docker-ready

## Setup (local)
1. Copy `.env.example` to `.env` and fill keys.
2. Backend:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
