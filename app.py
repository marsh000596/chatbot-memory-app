from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uuid
import os

import database
import models
import crud
import chatbot
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Chatbot with Memory API")
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "frontend")), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

chatbot_service = None

@app.on_event("startup")
def startup_event():
    global chatbot_service
																
    db = next(get_db())
    gpt4all_model_path = os.getenv("GPT4ALL_MODEL_PATH", "./models/ggml-gpt4all-j.bin")
    chatbot_service = chatbot.ChatbotService(db, gpt4all_model_path=gpt4all_model_path)

@app.post("/chat/")
def chat(
    question: str,
    user_id: str = None,
    domain: str = None,
    use_domain: bool = True,
    db: Session = Depends(get_db)
):
    if not user_id:
        # Generate a user id if not provided
        user_id = str(uuid.uuid4())
    
    # Store user message in memory
    crud.create_memory(db, user_id, question)

    # Get response
    response = chatbot_service.respond(user_id, question, domain, use_domain)

    # Store conversation record
    crud.create_conversation(db, user_id, question, response)

    return {"user_id": user_id, "response": response}
