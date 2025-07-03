import os
import time
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def is_valid_query(query: str, retries: int = 3, delay: int = 2) -> bool:
    """
    Uses Cohere's classify endpoint to determine if a query is 'valid' or 'invalid'.
    """
    inputs = [query]
    examples = [
        {"text": "How to start a startup?", "label": "valid"},
        {"text": "Latest news about AI tools", "label": "valid"},
        {"text": "asdfhjkl", "label": "invalid"},
        {"text": "search 123", "label": "invalid"},
        {"text": "Give me", "label": "invalid"},
        {"text": "what is", "label": "valid"},
        {"text": "explain blockchain", "label": "valid"},
        {"text": "How to do X in Python", "label": "valid"},
        {"text": "best programming languages 2025", "label": "valid"},
        {"text": "openai.com", "label": "invalid"}
    ]

    for attempt in range(retries):
        try:
            response = co.classify(
                inputs=inputs,
                examples=[cohere.ClassifyExample(e["text"], e["label"]) for e in examples]
            )
            prediction = response.classifications[0]
            top_label = prediction.prediction
            confidence = prediction.confidences[0].confidence

            print(f"🧠 Cohere Classifier: {top_label.upper()}, score={confidence:.2f}")
            return top_label == "valid"

        except Exception as e:
            print(f"❌ Cohere classification error (attempt {attempt+1}): {e}")
            time.sleep(delay * (2 ** attempt))  # Exponential backoff

    return False  # fallback if all attempts fail
