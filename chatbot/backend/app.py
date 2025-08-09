# app.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .crud import create_conversation, get_conversation, get_memory, add_domain_qa
from .chatbot import ChatbotService
from pydantic import BaseModel
import os

# Create DB tables automatically (for dev). For production use Alembic migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chatbot with Persistent Memory")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_service = ChatbotService()

class ChatRequest(BaseModel):
    conversation_id: int
    message: str
    domain: str = None
    use_domain: bool = False

@app.post("/start")
def start_conversation(title: str = "Conversation"):
    # create a new conversation
    conv = create_conversation(next(get_db()), title=title)  # quick create; better to use proper session
    return {"conversation_id": conv.id, "title": conv.title}

@app.post("/chat")
def chat(req: ChatRequest):
    # Validate conversation exists
    db = next(get_db())
    conv = db.query(models.Conversation).filter(models.Conversation.id == req.conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    result = chat_service.get_response(conversation_id=req.conversation_id, user_input=req.message, domain=req.domain, use_domain=req.use_domain)
    return result

@app.get("/history/{conversation_id}")
def history(conversation_id: int):
    db = next(get_db())
    conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = [{"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()} for m in conv.messages]
    return {"conversation_id": conversation_id, "messages": messages}

@app.post("/domain/add")
def add_domain(domain: str, question: str, answer: str):
    db = next(get_db())
    # For simplicity, not computing embedding here. Use data_loader for bulk imports with embeddings.
    qa = add_domain_qa(db, domain=domain, q=question, a=answer, embed_vec=None)
    return {"id": qa.id, "domain": qa.domain}

