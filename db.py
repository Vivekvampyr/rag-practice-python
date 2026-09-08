import psycopg2
from pgvector.psycopg2 import register_vector

DB_CONFIG = dict(
    dbname="rag-practice",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5434,
)

def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    register_vector(conn)
    return conn
