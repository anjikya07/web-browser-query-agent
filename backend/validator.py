from transformers import pipeline
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Access token
hf_token = os.getenv("HF_TOKEN")

# Load once at module level, with authentication
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    token=hf_token  # ✅ REQUIRED for access
)

def is_valid_query(query: str) -> bool:
    candidate_labels = ["valid", "invalid"]

    try:
        result = classifier(query, candidate_labels)
        label = result["labels"][0]
        score = result["scores"][0]

        print(f"⚙️ HF Validator: {label.upper()}, score={score:.2f}")
        return label == "valid"
    except Exception as e:
        print("❌ Hugging Face classification error:", e)
        return False
