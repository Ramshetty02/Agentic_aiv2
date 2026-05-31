import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"}

def search_web(query: str) -> str:
    """Search DuckDuckGo and return HTML for link extraction."""
    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        return f"Search failed: {e}"

def scrape_page(url: str, max_chars: int = 3000) -> str:
    """Scrape and clean text content from a URL."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return " ".join(soup.get_text(separator=" ").split())[:max_chars]
    except Exception:
        return ""
