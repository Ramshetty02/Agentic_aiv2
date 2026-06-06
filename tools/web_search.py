import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"}


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Search DuckDuckGo and return structured results."""
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        return [{"title": "Search failed", "href": "", "body": str(e)}]


def scrape_page(url: str, max_chars: int = 3000) -> str:
    """Scrape and clean text content from a URL."""
    if not url:
        return ""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return " ".join(soup.get_text(separator=" ").split())[:max_chars]
    except Exception:
        return ""
