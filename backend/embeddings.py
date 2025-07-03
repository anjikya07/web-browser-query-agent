import json
import numpy as np
import os
import cohere
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_FILE = "embeddings.json"
co = cohere.Client(api_key=os.getenv("CO_API_KEY"))


def get_embedding(query: str):
    try:
        response = co.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"  # 👈 required now!
        )
        return response.embeddings[0]
    except Exception as e:
        print("❌ Embedding error:", e)
        return [0.0] * 1024  # fallback dummy vector


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def load_embeddings():
    try:
        with open(EMBEDDING_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_embeddings(data):
    with open(EMBEDDING_FILE, "w") as f:
        json.dump(data, f, indent=2)

def find_similar_query(query, threshold=0.90):
    embeddings = load_embeddings()
    new_embedding = get_embedding(query)

    for past_query, emb in embeddings.items():
        if cosine_similarity(emb, new_embedding) >= threshold:
            return past_query, new_embedding
    return None, new_embedding
