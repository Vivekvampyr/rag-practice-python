import json
import numpy as np
from sentence_transformers import SentenceTransformer

class KnowledgeBase:
    def __init__(self, path="knowledge_base_150_python.json"):
        with open(path, "r") as f:
            self.data = json.load(f)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.corpus_texts = [
            item["question"] + " " + " ".join(item["answer"])
            for item in self.data
        ]
        print("Embedding knowledge_base...")
        self.embeddings = self.model.encode(self.corpus_texts, normalize_embeddings=True)

    def search(self, query: str, k_top: int = 3):
        query_vec = self.model.encode([query],normalize_embeddings=True)[0]
        scores = self.embeddings @ query_vec
        top_idx = np.argsort(scores)[::-1][:k_top]
        return [
            {
                "question": self.data[i]["question"],
                "answer": self.data[i]["answer"],
                "score": float(scores[i])
            }
            for i in top_idx
        ]
