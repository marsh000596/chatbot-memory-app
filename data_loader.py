import csv
from sqlalchemy.orm import Session
from .crud import add_domain_qa

def load_domain_qa_from_csv(db: Session, filepath: str, domain: str):
    """
    Load domain question-answer pairs from a CSV file with columns: question, answer
    """
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            question = row.get("question")
            answer = row.get("answer")
            if question and answer:
                add_domain_qa(db, domain, question, answer)
