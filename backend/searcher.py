import logging
import json
import os
from urllib.parse import quote_plus
from playwright.sync_api import sync_playwright

CACHE_FILE = "search_cache.json"
logger = logging.getLogger(__name__)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def startpage_search(query):
    urls = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--single-process",
                "--disable-setuid-sandbox",
                "--disable-extensions",
                "--disable-background-networking",
                "--mute-audio",
                "--metrics-recording-only",
                "--no-first-run",
                "--disable-sync",
                "--disable-default-apps",
                "--enable-automation"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )
        page = context.new_page()

        try:
            search_url = f"https://www.startpage.com/do/search?query={quote_plus(query)}"
            page.goto(search_url, timeout=30000)
            page.wait_for_timeout(4000)

            anchors = page.locator("a.result-link").all()
            for anchor in anchors:
                href = anchor.get_attribute("href")
                if href and href.startswith("http"):
                    urls.append(href)
                if len(urls) >= 5:
                    break

        except Exception as e:
            print(f"❌ Startpage search error: {e}")
            logger.exception("Startpage search failed")
        finally:
            browser.close()

    return urls

def smart_search(query):
    cache = load_cache()

    if query in cache:
        print("\n📦 Found cached search results.")
        return cache[query]["urls"], cache[query]["engine"]

    try:
        print("\n🔍 Using Startpage Search (Google powered)...")
        urls = startpage_search(query)
        if urls:
            cache[query] = {"urls": urls, "engine": "Startpage"}
            save_cache(cache)
            return urls, "Startpage"
        else:
            raise Exception("No URLs from Startpage")
    except Exception as e:
        print(f"\n❌ Startpage failed: {e}")
        raise
