import json
from sentence_transformers import SentenceTransformer
from psycopg2.extras import execute_values
from db import get_connection

model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest(json_path: str = "knowledge_base.json", batch_size: int = 256):
    with open(json_path) as f:
        data = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        texts = [item["question"] + " " + item["answer"] for item in batch]

        embedding = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        rows = [
            (item.get("category"), item["question"], item["answer"], emb.tolist())
            for item, emb in zip(batch, embedding)
        ]

        execute_values(
            cur,
            "INSERT INTO knowledge_base (category, question, answer, embedding) VALUES %s",
            rows,
            template="(%s, %s, %s, %s::vector)"
        )
        conn.commit()
        print(f"Ingested {i + len(batch)} / {len(data)}")

    cur.close()
    conn.close()
    print(f"Done. Ingested {len(data)} enteries total.")
if __name__ == "__main__":
    ingest()