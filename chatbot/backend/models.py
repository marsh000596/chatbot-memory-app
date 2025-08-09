# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="Conversation")
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Memory", back_populates="conversation", cascade="all, delete-orphan")

class Memory(Base):
    __tablename__ = "memory"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    role = Column(String, index=True)  # 'user' or 'bot'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class DomainQA(Base):
    __tablename__ = "domain_qa"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)   # e.g., 'healthcare', 'finance', 'customer_service'
    question = Column(Text)
    answer = Column(Text)
    # optional embedding fields for semantic search
    embedding = Column(Text, nullable=True)  # store as JSON string or comma-separated floats
    created_at = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float, default=1.0)  # optional metadata
