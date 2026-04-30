from tavily import TavilyClient
from config import TAVILY_API_KEY

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(query):
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return []

    structured_results = []

    for r in results:
        structured_results.append({
            "title": r.get("title"),
            "content": r.get("content"),
            "url": r.get("url")
        })

    return structured_results
