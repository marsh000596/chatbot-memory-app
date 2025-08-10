# Chatbot with Persistent Memory
- This project is a domain-specific chatbot with persistent memory built using FastAPI for the backend and a simple web frontend.
- It supports offline LLM integration (e.g., GPT4All), semantic search over domain knowledge, and stores conversation history in a database.
- A full-stack demo: FastAPI backend, SQLite persistent memory, domain Q&A, and a web GUI.

## Features
- Persistent conversations & memory (SQLite)
- Domain-specific knowledge base (DomainQA)
- Optional semantic search over domain Q/A
- LLM integration (OpenAI by default; fallback to HF/local)
- Simple web frontend (vanilla HTML/CSS/JS)
- Docker-ready

## Prerequisites
- Python 3.9+ installed (if running backend locally)
- Docker and Docker Compose installed (optional, for containerized setup)
- Internet connection for first-time GPT4All model download (optional)

## Setup (local)
- Copy `.env.example` to `.env` and fill keys.
   ```graphql
   chatbot-memory-app/
   │
   ├── __init__.py
   ├── app.py                 # FastAPI entrypoint (runs API)
   ├── chatbot.py              # Chatbot logic + memory & domain selection
   ├── database.py             # SQLAlchemy engine + session
   ├── models.py               # DB models
   ├── crud.py                 # DB helper functions
   ├── data_loader.py          # Loads Q&A into DB
   ├── requirements.txt
   ├── Dockerfile
   │
   ├── frontend/
   │   ├── index.html
   │   ├── style.css
   │   ├── script.js
   │
   ├── models/
   │   └── gpt4all-model.bin       # Your offline GPT4All model file
   │
   ├── docker-compose.yml
   ├── README.md
   └── .env.example



## Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/marsh000596/chatbot-memory-app.git #once published, currently the files/folder can be downloaded manually
cd chatbot-memory-app
```

2. Prepare environment variables
Copy .env.example to .env in the backend folder and adjust if needed:
```bash
cp backend/.env.example backend/.env
```
The default .env for GPT4All looks like:
```env
LLM_PROVIDER=gpt4all
GPT4ALL_MODEL=orca-mini-3b.ggmlv3.q4_0.bin
DATABASE_URL=sqlite:///./chatbot.db
EMBEDDING_MODEL=all-MiniLM-L6-v2
OPENAI_API_KEY=             # leave empty if not using OpenAI
```
Also save a bin for local chatgpt in /models
```
wget https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin -O gpt4all-model.bin
#or visit https://gpt4all.io/index.html?ref=top-ai-list and install gpt4all to get any of your choice
```

3. Running with Docker Compose (recommended)
This will build and start the backend in a Docker container:
```bash
docker-compose -f backend/docker-compose.yml up --build
```
- Backend API will be available at: http://localhost:8000
- You can view API docs at: http://localhost:8000/docs

4. Serving the frontend
You have two options:
- Open frontend/index.html directly in your browser (works fine for local testing)
- Or serve via Python HTTP server for full functionality:
```bash
cd frontend
python -m http.server 5500
```
Then open ```http://localhost:5500/index.html in your browser.```

optional:
- setup env:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   

## How to Use
- Type your message in the chat input box.
- Use the "Use Domain Data" toggle to choose whether the chatbot answers from your domain knowledge or uses the local LLM fallback.
- The chatbot remembers conversation history, allowing context-aware replies.

## Folder and File Breakdown

/backend/ — Backend API and Core Logic
app.py
- The main entrypoint for the backend server.
- It creates and runs the FastAPI application, sets up routing, and exposes API endpoints for the chatbot frontend to communicate with.
- Need: Without this, there is no running API server.

chatbot.py
- Contains the core chatbot logic.
  Handles:
  - User message processing
  - Retrieving relevant domain knowledge using semantic similarity
  - Managing conversation memory
  - Interacting with the language model (local GPT4All or OpenAI)
    - Need: This is the brain of the chatbot, connecting memory and LLM.

database.py
- Configures the SQLAlchemy engine and session for the database.
- It manages the connection to the SQLite database (or another DB) where conversation memory and domain Q&A are stored.
- Need: Enables persistent storage for conversation state.

models.py
- Defines the database schema via SQLAlchemy ORM models.
- Contains models like Memory, DomainQA, and Conversation which represent chatbot memory entries, domain-specific Q&A pairs, and conversations respectively.
- Need: The blueprint for how data is stored and accessed.

crud.py
- Contains helper functions to perform create, read, update, delete operations on the database models.
- Functions include adding memories, fetching conversation history, and querying domain knowledge.
- Need: Abstracts database operations for cleaner code.

data_loader.py
- Utility script for bulk loading domain-specific Q&A data into the database.
- Useful to import knowledge bases (like CSV files) so your chatbot can answer domain questions.
- Optional: You may add data validation or transform features here.

requirements.txt
- Lists all Python dependencies required to run the backend, such as FastAPI, SQLAlchemy, GPT4All, Transformers, and more.
- Need: Simplifies setup by letting you install all packages with pip install -r requirements.txt.

Dockerfile
- Defines how to containerize the backend app into a Docker image.
- Specifies base Python image, copies source code, installs dependencies, and sets the command to start the FastAPI server.
- Optional: Can be enhanced with multi-stage builds, security best practices.

docker-compose.yml
- Defines how to run the backend container with Docker Compose.
- Includes environment variables, port mappings, and volume mounts.
- Useful for quick startup and orchestration.
- Optional: Could be extended to add other services like a frontend server, database containers, or monitoring.

/frontend/ — Frontend Web Interface

index.html
- The main webpage for users to interact with the chatbot.
- Includes the chat window, input box, buttons, and UI structure.
- Need: Without this, no user interface.

style.css
- Contains styles and layout rules to make the chat UI look clean and user-friendly.
- Optional: You can add themes, animations, responsive design here.

script.js
- JavaScript code that manages frontend behavior:
- Captures user input
- Sends API requests to backend
- Displays chatbot responses dynamically
- Handles toggling options like "Use Domain Data"
  - Need: Enables interactive chat experience.

Root Files

README.md
- This file (or similar) explaining project purpose, setup instructions, and structure.
- Need: Important for anyone new to the project to get started.

.env.example
- Sample environment variable file demonstrating required config variables (like database URL, LLM model choice, API keys).
- Optional: Helps configure your app without hardcoding secrets.

## Optional Features You Can Add Later

- Authentication & User Accounts
- Allow users to log in and save their own conversation histories.
Multi-domain Support
- Let users select different knowledge domains (e.g., healthcare, finance) dynamically.
Advanced Memory Management
- Implement memory summarization, forgetting older context, or priority-based retrieval.
Enhanced Frontend
- Add voice input/output, chat history, rich media support (images, videos).
Monitoring and Analytics
- Track chatbot usage, response quality, error logging.
Deployment Automation
- CI/CD pipelines, automated testing, Kubernetes deployment.
Database Choices
- Swap SQLite for PostgreSQL or cloud-managed DBs for scalability.
Model Options
- Integrate other LLMs, or fine-tune models on your domain data.
Caching & Rate Limiting
- Improve performance and prevent abuse.
Troubleshooting
- If GPT4All model download stalls, try downloading manually and placing the model file where .env expects it.
##
- Make sure .env variables match your environment and Docker setup.
- Check backend logs (docker-compose logs) for errors.

## Summary
This project is designed to be a flexible foundation for a domain-specific chatbot that can be extended and customized easily.
Each file serves a clear purpose from backend API, data management, AI logic, to frontend UI.
