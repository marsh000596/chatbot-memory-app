import os
from typing import Optional
from sqlalchemy.orm import Session
import crud
from gpt4all import GPT4All
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


class ChatbotService:
    def __init__(
        self,
        db: Session,
        embedder_model: str = "all-MiniLM-L6-v2",
        gpt4all_model_path: Optional[str] = None
    ):
        self.db = db
        self.embedder = SentenceTransformer(embedder_model)
        self.index = None
        self.domain_qas = []
        self.domain_embeddings = None
        self.gpt_model = None

        if gpt4all_model_path and os.path.exists(gpt4all_model_path):
            ext = os.path.splitext(gpt4all_model_path)[1].lower()
            if ext == ".gguf":
                print(f"Loading GGUF model via llama.cpp from {gpt4all_model_path} ...")
                self.gpt_model = Llama(model_path=gpt4all_model_path, n_ctx=2048)
            elif ext == ".bin":
                print(f"Loading GPT4All legacy .bin model from {gpt4all_model_path} ...")
                self.gpt_model = GPT4All(model_name=gpt4all_model_path)
            else:
                raise ValueError(f"Unsupported model format: {ext}")
        else:
            print("No valid model path found, GPT fallback disabled.")

    def load_domain_data(self, domain: str):
        qas = crud.get_domain_qa(self.db, domain)
        self.domain_qas = [(qa.question, qa.answer) for qa in qas]
        if self.domain_qas:
            questions = [q for q, _ in self.domain_qas]
            self.domain_embeddings = self.embedder.encode(questions, convert_to_numpy=True)
            dimension = self.domain_embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.domain_embeddings)
        else:
            self.index = None

    def get_best_domain_answer(self, user_question: str, threshold=0.6) -> Optional[str]:
        if not self.index:
            return None
        question_embedding = self.embedder.encode([user_question], convert_to_numpy=True)
        D, I = self.index.search(question_embedding, k=1)
        score = D[0][0]
        best_idx = I[0][0]
        if score < threshold:
            return self.domain_qas[best_idx][1]
        return None

    def respond(self, user_id: str, question: str, domain: Optional[str] = None, use_domain: bool = True):
        # Step 1: Domain knowledge
        if domain and use_domain:
            self.load_domain_data(domain)
            domain_answer = self.get_best_domain_answer(question)
            if domain_answer:
                return domain_answer

        # Step 2: Model inference
        if self.gpt_model:
            if isinstance(self.gpt_model, Llama):
                output = self.gpt_model(
                    question,
                    max_tokens=512,
                    stop=["</s>"],
                    echo=False
                )
                return output["choices"][0]["text"].strip()
            elif isinstance(self.gpt_model, GPT4All):
                return self.gpt_model.generate(question)

        # Step 3: Fallback
        return f"General response to: {question}"
