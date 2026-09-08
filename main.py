from fastapi import FastAPI
from pydantic import BaseModel
from rag import KnowledgeBase

app = FastAPI(title="Welcome to RAG implementation")
kb = KnowledgeBase("knowledge_base_150_python.json")

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Welcome to RAG Implementation"}

@app.post("/ask")
def ask(query: Query):
    matches = kb.search(query.question, k_top=1)[0]
    best = max(matches, )
    return {
        "question": matches["question"],
        "answer": matches["answer"],
        "score": matches["score"]
        }