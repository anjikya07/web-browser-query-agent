import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

def is_valid_query(query: str, retries: int = 3, timeout: int = 30) -> bool:
    """
    Classifies a query as 'valid' or 'invalid' using Hugging Face's zero-shot API.
    Retries on timeout or connection errors.
    """
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

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=timeout)
            response.raise_for_status()

            result = response.json()
            label = result["labels"][0]
            score = result["scores"][0]

            print(f"✅ Hugging Face classified as: {label.upper()} (score={score:.2f})")
            return label == "valid"

        except requests.exceptions.Timeout:
            print(f"⚠️ Timeout on attempt {attempt}/{retries}. Retrying in {2**attempt} sec...")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error on attempt {attempt}/{retries}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

        time.sleep(2 ** attempt)  # Exponential backoff

    print("❌ Hugging Face classification failed after retries.")
    return False
