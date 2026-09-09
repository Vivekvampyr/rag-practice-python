import logging
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from rag import retrieve
from generate import generate_answer, generate_answer_stream

logger = logging.getLogger(__name__)
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
    try:
        final_answer = generate_answer(query.question, matches)
        generated = True
    except Exception as e:
        logger.warning(f"Gemini generation failed, falling back to raw match: {e}")
        final_answer = best["answer"]
        generated = False
        

    return {
        "answer": final_answer,
        "matched_question": best["question"],
        "score": best["score"],
        "matched": True,
        "ai_generated": generated,
        "sources": matches,
        }

@app.post("/ask/stream")
def ask_stream(query: Query):
    matches = retrieve(query.question, top_k=3, similarity_threshold=0.5)

    if not matches:
        def no_match():
            yield "Sorry, I don't have information on that."
        return StreamingResponse(no_match(), media_type="text/plain")
    def event_generator():
        try:
            for chunk in generate_answer_stream(query.question, matches):
                yield chunk
        except Exception:
            yield f"\n\n[Note: AI generation failed, showing raw match instead]\n{matches[0]['answer']}"

    return StreamingResponse(event_generator(), media_type="text/plain")