from rag.query import search_games
from web_search import web_search


def retrieve_game(query):
    results = search_games(query)

    return {
        "tool": "retrieve_game",
        "query": query,
        "results": results
    }


def evaluate_retrieval(results):
    if not results:
        return {
            "tool": "evaluate_retrieval",
            "status": "fail",
            "reason": "No results found"
        }

    return {
        "tool": "evaluate_retrieval",
        "status": "pass",
        "reason": "Results look usable"
    }


def game_web_search(query):
    results = web_search(query)

    return {
        "tool": "game_web_search",
        "query": query,
        "results": results
    }
