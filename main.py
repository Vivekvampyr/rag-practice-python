from fastapi import FastAPI
from pydantic import BaseModel
from rag import retrieve

app = FastAPI(title="Welcome to RAG implementation")

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Welcome to RAG Implementation"}

@app.post("/ask")
def ask(query: Query):
    matches = retrieve(query.question, top_k=3, similarity_threshold=0.5)
    if not matches:
        return {"answer": "Sorry, I don't have information on that.", "matched": False}
    
    best = matches[0]

    return {
        "answer": best["answer"],
        "matched_question": best["question"],
        "category": best["category"],
        "score": best["score"],
        "matched": True,
        "other_candidates": matches[1:]
        }