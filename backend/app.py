from flask import Flask, request, jsonify
from flask_cors import CORS
from validator import is_valid_query
from embeddings import find_similar_query, load_embeddings, save_embeddings
from searcher import smart_search
from summarizer import extract_text, summarize
import json
import os

app = Flask(__name__)
CORS(app)

CACHE_FILE = "cache.json"

def load_cache():
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/query", methods=["POST"])
def handle_query():
    data = request.json
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "No query provided."}), 400

    if not is_valid_query(query):
        return jsonify({"valid": False, "message": "Invalid query"}), 200

    embeddings_db = load_embeddings()
    cache = load_cache()

    similar_query, new_embedding = find_similar_query(query)
    if similar_query in cache:
        return jsonify({"valid": True, "cached": True, "result": cache[similar_query]}), 200

    try:
        urls, engine = smart_search(query)
    except Exception:
        return jsonify({"error": "Search failed"}), 500

    summaries = []
    for url in urls:
        text = extract_text(url)
        if text:
            summary = summarize(text)
            if summary:
                summaries.append({"url": url, "summary": summary})

    if summaries:
        combined = "\n\n".join(f"{s['url']}\n{s['summary']}" for s in summaries)
        cache[query] = combined
        save_cache(cache)
        embeddings_db[query] = new_embedding
        save_embeddings(embeddings_db)
        return jsonify({"valid": True, "cached": False, "result": combined}), 200
    else:
        return jsonify({"valid": True, "cached": False, "result": "No useful content found."}), 200

if __name__ == "__main__":
    app.run(debug=True)
