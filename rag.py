from sentence_transformers import SentenceTransformer
from db import get_connection

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query: str, top_k: int = 3, similarity_threshold: float = 0.5):
    query_embedding = model.encode(query,normalize_embeddings=True)
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SET hnsw.ef_search = 40;")
    cur.execute(
        """
        SELECT question, answer, category, 1 - (embedding <=> %s) AS similarity
        FROM knowledge_base
        ORDER BY embedding <=> %s
        LIMIT %s
        """,
        (query_embedding, query_embedding, top_k)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    results = [
        {"question": r[0], "answer": r[1], "category": r[2], "score": float(r[3])}
        for r in rows
    ]
    return [r for r in results if r["score"] >= similarity_threshold]
