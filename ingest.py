import json
from sentence_transformers import SentenceTransformer
from db import get_connection

model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest(json_path: str = "knowledge_base.json"):
    with open(json_path) as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()
    for item in data:
        text_to_embed = item["question"] + " " + item["answer"]
        embedding = model.encode(text_to_embed,normalize_embeddings=True)
        cur.execute(
            """
            INSERT INTO knowledge_base (category, question, answer, embedding)
            VALUES (%s, %s, %s, %s)
            """,
            (item.get("category"), item["question"], item["answer"], embedding)
        )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Ingested {len(data)} enteries. ")
if __name__ == "__main__":
    ingest()