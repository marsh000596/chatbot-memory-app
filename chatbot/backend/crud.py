# crud.py
import json
from sqlalchemy.orm import Session
from . import models
from sentence_transformers import SentenceTransformer
import numpy as np

# optional: in-memory embedding model for domain search (if stored embedding absent)
_embedding_model = None
def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model

def create_conversation(db: Session, title: str = "Conversation"):
    conv = models.Conversation(title=title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

def get_conversation(db: Session, conv_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conv_id).first()

def add_memory(db: Session, conversation_id: int, role: str, content: str):
    mem = models.Memory(conversation_id=conversation_id, role=role, content=content)
    db.add(mem)
    db.commit()
    db.refresh(mem)
    return mem

def get_memory(db: Session, conversation_id: int, limit: int = 50):
    return db.query(models.Memory).filter(models.Memory.conversation_id == conversation_id).order_by(models.Memory.timestamp).limit(limit).all()

def add_domain_qa(db: Session, domain: str, q: str, a: str, embed_vec: list = None):
    embedding_json = json.dumps(embed_vec) if embed_vec is not None else None
    qa = models.DomainQA(domain=domain, question=q, answer=a, embedding=embedding_json)
    db.add(qa)
    db.commit()
    db.refresh(qa)
    return qa

def find_domain_match_semantic(db: Session, domain: str, query: str, top_k: int = 1):
    """
    Naive semantic search using stored embeddings or compute on the fly.
    Returns best match or None.
    """
    # load QAs for that domain
    qas = db.query(models.DomainQA).filter(models.DomainQA.domain == domain).all()
    if not qas:
        return None, 0.0

    # load embeddings if present
    vectors = []
    ids = []
    for q in qas:
        if q.embedding:
            vec = json.loads(q.embedding)
            vectors.append(vec)
            ids.append(q.id)

    model = _get_embedding_model()
    q_vec = model.encode([query])[0]

    if vectors:
        # compute cosine similarity
        vectors = np.array(vectors)
        qv = np.array(q_vec)
        # normalize
        vectors_norm = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        qv_norm = qv / np.linalg.norm(qv)
        sims = (vectors_norm @ qv_norm).tolist()
        best_idx = int(np.argmax(sims))
        best_id = ids[best_idx]
        best_sim = sims[best_idx]
        best_qa = next((x for x in qas if x.id == best_id), None)
        return best_qa, float(best_sim)
    else:
        # fallback: simple substring match / heuristic
        for q in qas:
            if query.lower() in q.question.lower() or any(w in q.question.lower() for w in query.lower().split()):
                return q, 0.6
        return None, 0.0
