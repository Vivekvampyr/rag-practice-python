import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def build_prompt(query: str, matches: list) -> str:
    context = "\n\n".join(
        f"Q: {m['question']}\nA: {m['answer']}" for m in matches
    )
    return f"""Answer the user's question using ONLY the context below.
    If the context doesn't contain the answer, say you don't know.
    Context:
    {context}
    Question: {query}"""

def generate_answer(query: str, matches: list) -> str:
    """Non-streaming version -- used for the fallback path."""
    prompt = build_prompt(query, matches)
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )
    return response.text

def generate_answer_stream(query: str, matches: list):
    """Yields text chunks as Gemini generates them."""
    prompt = build_prompt(query, matches)
    for chunk in client.models.generate_content_stream(model="gemini-3.1-flash-lite",contents=prompt):
        if chunk.text:
            yield chunk.text