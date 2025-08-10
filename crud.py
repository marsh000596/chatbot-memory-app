from sqlalchemy.orm import Session
import models

# Memory CRUD
def create_memory(db: Session, user_id: str, message: str):
    memory = models.Memory(user_id=user_id, message=message)
    db.add(memory)
    db.commit()
    db.refresh(memory)
    return memory

def get_user_memory(db: Session, user_id: str):
    return db.query(models.Memory).filter(models.Memory.user_id == user_id).all()

# Domain QA CRUD
def get_domain_qa(db: Session, domain: str):
    return db.query(models.DomainQA).filter(models.DomainQA.domain == domain).all()

def add_domain_qa(db: Session, domain: str, question: str, answer: str):
    qa = models.DomainQA(domain=domain, question=question, answer=answer)
    db.add(qa)
    db.commit()
    db.refresh(qa)
    return qa

# Conversation CRUD
def create_conversation(db: Session, user_id: str, question: str, answer: str):
    conv = models.Conversation(user_id=user_id, question=question, answer=answer)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_user_conversations(db: Session, user_id: str):
    return db.query(models.Conversation).filter(models.Conversation.user_id == user_id).all()
