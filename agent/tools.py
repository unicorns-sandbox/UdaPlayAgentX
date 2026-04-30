from rag.query import semantic_search

def retrieve_game(query):
    return semantic_search(query)

def evaluate_retrieval(result):
    if not result or len(result[0]) == 0:
        return 0.2
    return 0.85

from web.tavily_search import search_web

def game_web_search(query):
    return search_web(query)