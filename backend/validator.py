import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

def is_valid_query(query: str) -> bool:
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": query,
        "parameters": {
            "candidate_labels": ["valid", "invalid"]
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        label = result["labels"][0]
        score = result["scores"][0]
        print(f"⚙️ Hugging Face Validator: {label.upper()}, score={score:.2f}")

        return label == "valid"
    except Exception as e:
        print("❌ Hugging Face API error:", e)
        return False
