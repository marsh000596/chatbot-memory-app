# chatbot.py
import os
from typing import Optional
from .crud import add_memory, get_memory, find_domain_match_semantic
from .database import SessionLocal
from dotenv import load_dotenv
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gpt4all")  # default to gpt4all

# GPT4All wrapper
def call_gpt4all(prompt: str) -> str:
    from gpt4all import GPT4All
    model_path = os.getenv("GPT4ALL_MODEL", "orca-mini-3b.ggmlv3.q4_0.bin")
    model = GPT4All(model_path)
    with model.chat_session():
        return model.generate(prompt, max_tokens=200)

class ChatbotService:
    def __init__(self):
        pass

    def get_response(self, conversation_id: int, user_input: str, domain: Optional[str] = None, use_domain: bool = False):
        db = SessionLocal()
        try:
            # 1. Save user message
            add_memory(db, conversation_id=conversation_id, role="user", content=user_input)

            # 2. Domain-based answer (if requested)
            if use_domain and domain:
                best_qa, sim = find_domain_match_semantic(db, domain=domain, query=user_input)
                if best_qa and sim and sim >= 0.65:
                    answer = best_qa.answer
                    add_memory(db, conversation_id=conversation_id, role="bot", content=answer)
                    return {"response": answer, "source": "domain", "score": sim}

            # 3. Fallback to LLM (GPT4All)
            last_messages = get_memory(db, conversation_id=conversation_id, limit=20)
            context = "".join(f"{m.role}: {m.content}\n" for m in last_messages)
            full_prompt = f"{context}\nuser: {user_input}\nbot:"

            reply = call_gpt4all(full_prompt)

            add_memory(db, conversation_id=conversation_id, role="bot", content=reply)
            return {"response": reply, "source": "llm", "score": None}
        finally:
            db.close()
