import os
import requests
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_SUMMARIZE_URL = "https://api.cohere.ai/v1/summarize"

HEADERS = {
    "Authorization": f"Bearer {COHERE_API_KEY}",
    "Content-Type": "application/json"
}

def extract_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join(p.get_text(strip=True) for p in paragraphs)


        return text[:10000]  # Max content limit for Cohere summarization
    except Exception as e:
        print(f"⚠️ Extraction error for {url}: {e}")
        return None

def summarize(text, retries=3):
    if not text:
        return None

    for attempt in range(retries):
        try:
            payload = {
                "text": text,
                "length": "medium",  # Options: short, medium, long
                "format": "paragraph",  # or "bullets"
                "model": "summarize-xlarge"  # Free-tier compatible
            }

            response = requests.post(COHERE_SUMMARIZE_URL, headers=HEADERS, json=payload)

            if response.status_code == 200:
                summary = response.json().get("summary")
                if summary:
                    return summary.strip()
            else:
                print(f"[Retry {attempt+1}] HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[Retry {attempt+1}] Exception: {e}")
        time.sleep(2 ** attempt)

    return None
