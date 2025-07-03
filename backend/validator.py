import os
import cohere
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

def is_valid_query(query: str) -> bool:
    prompt = f"""Classify the following user query as either "valid" or "invalid" based on whether it is clear, useful, and makes sense for a web search:

Query: "{query}"
Answer:"""

    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=5,
            temperature=0.2,
            stop_sequences=["\n"]
        )
        output = response.generations[0].text.strip().lower()
        print(f"🧠 LLM output: '{output}'")
        return "valid" in output
    except Exception as e:
        print("❌ Cohere Command R error:", e)
        return False
