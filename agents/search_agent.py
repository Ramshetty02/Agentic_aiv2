from tools.web_search import search_web, scrape_page
from bs4 import BeautifulSoup

def search_agent(query: str) -> dict:
    """Multi-source search: DuckDuckGo HTML + BeautifulSoup page scraping."""
    results = {"query": query, "web_results": [], "raw_content": ""}

    raw_html = search_web(query)
    soup = BeautifulSoup(raw_html, "html.parser")
    links = [
        a["href"] for a in soup.find_all("a", href=True)
        if "http" in a.get("href", "") and "duckduckgo" not in a["href"]
    ][:5]

    for link in links:
        content = scrape_page(link)
        if content:
            results["web_results"].append({"url": link, "snippet": content[:500]})

    results["raw_content"] = "\n\n".join(r["snippet"] for r in results["web_results"])
    return results
