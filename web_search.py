from tavily import TavilyClient
from config import TAVILY_API_KEY

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query):
   
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return {
            "query": query,
            "answer": "No results found.",
            "source": "Tavily"
        }

    # Format results into readable text
    formatted = []
    for r in results:
        formatted.append(f"- {r['title']}: {r['content']}")

    return {
        "query": query,
        "answer": "\n".join(formatted),
        "source": "Tavily",
        "raw_results": results
    }