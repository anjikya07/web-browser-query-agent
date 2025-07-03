import os
import time
import cohere
from dotenv import load_dotenv

load_dotenv()

CO_API_KEY = os.getenv("CO_API_KEY")
co = cohere.Client(CO_API_KEY)

def is_valid_query(query: str, retries: int = 3, threshold: float = 0.5) -> bool:
    examples = [
        cohere.ClassifyExample(text="What is AI?", label="valid"),
        cohere.ClassifyExample(text="How to learn machine learning?", label="valid"),
        cohere.ClassifyExample(text="Python programming tutorials", label="valid"),
        cohere.ClassifyExample(text="asdfghjkl", label="invalid"),
        cohere.ClassifyExample(text="!!!@#$$", label="invalid"),
        cohere.ClassifyExample(text="kjhqwieuqwe", label="invalid"),
    ]

    for attempt in range(retries):
        try:
            response = co.classify(
                inputs=[query],
                examples=examples,
            )
            prediction = response.classifications[0]
            label = prediction.prediction
            confidence = prediction.confidence

            print(f"🧠 Cohere: '{label.upper()}' with confidence {confidence:.2f}")

            return label == "valid" and confidence >= threshold
        except Exception as e:
            print(f"❌ Cohere classification error (attempt {attempt + 1}): {e}")
            time.sleep(2 ** attempt)

    return False
