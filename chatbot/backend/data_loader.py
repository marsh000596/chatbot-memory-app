# data_loader.py
# Utility script to bulk load domain Q&A from CSV or JSON into DB
import csv
import json
from sqlalchemy.orm import Session
from .crud import add_domain_qa, _get_embedding_model

def load_from_csv(db: Session, csv_path: str, domain_column="domain", qcol="question", acol="answer", compute_embeddings=True):
    model = _get_embedding_model() if compute_embeddings else None
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = row.get(domain_column, "default")
            q = row.get(qcol, "")
            a = row.get(acol, "")
            embed = None
            if compute_embeddings and q:
                embed = model.encode([q])[0].tolist()
            add_domain_qa(db, domain=domain, q=q, a=a, embed_vec=embed)
    print("Loaded CSV into DB.")
