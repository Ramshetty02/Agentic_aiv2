from agents.plan_schema import ResearchPlan
from tools.web_search import search_web, scrape_page


def _search_queries(query: str, plan: ResearchPlan | None) -> list[str]:
    """Build search queries from the user task and planner output."""
    queries = [query]
    if plan:
        queries.extend(plan.key_questions[:3])
    seen = set()
    unique = []
    for q in queries:
        normalized = q.strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique.append(q.strip())
    return unique[:4]


def search_agent(query: str, plan: ResearchPlan | None = None) -> dict:
    """Multi-source search driven by the research plan."""
    results = {
        "query": query,
        "plan_objective": plan.objective if plan else query,
        "search_queries": [],
        "web_results": [],
        "raw_content": "",
    }

    seen_urls: set[str] = set()
    for search_query in _search_queries(query, plan):
        results["search_queries"].append(search_query)
        for hit in search_web(search_query, max_results=3):
            url = hit.get("href", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            snippet = hit.get("body", "")
            page_content = scrape_page(url)
            content = page_content or snippet

            if content:
                results["web_results"].append({
                    "url": url,
                    "title": hit.get("title", ""),
                    "search_query": search_query,
                    "snippet": content[:500],
                })

            if len(results["web_results"]) >= 8:
                break
        if len(results["web_results"]) >= 8:
            break

    results["raw_content"] = "\n\n".join(
        f"[{r['title']}] ({r['url']})\n{r['snippet']}"
        for r in results["web_results"]
    )
    return results
