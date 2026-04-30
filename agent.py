from rag import retrieve_local
from web_search import search_web
from evaluator import evaluate
from memory import save_to_memory

# ---------------------------
# Reporting / Output Formatter
# ---------------------------
def format_response(query, data, source, confidence, reasoning):
    return f"""
🎮 UdaPlay Report
----------------------
Query: {query}

Reasoning:
{chr(10).join(reasoning)}

Source: {source}
Confidence: {confidence:.2f}

Answer:
{data}
"""

# ---------------------------
# Agent Class
# ---------------------------
class UdaPlayAgent:

    def __init__(self):
        self.history = []  # stateful memory

    def answer(self, query):

        reasoning = []

        # ---------------------------
        # STATE 1: RETRIEVE (RAG)
        # ---------------------------
        local_data = retrieve_local(query)
        reasoning.append("Used retrieve_game (RAG)")

        # ---------------------------
        # STATE 2: EVALUATE
        # ---------------------------
        confidence = evaluate(local_data)
        reasoning.append(f"Evaluation score: {confidence}")

        # ---------------------------
        # STATE 3: DECIDE / FALLBACK
        # ---------------------------
        if confidence < 0.6:
            reasoning.append("Low confidence → using web search")

            web_data = search_web(query)
            save_to_memory(web_data)

            response = format_response(
                query,
                web_data,
                "Web Search (Tavily)",
                0.4,
                reasoning
            )

        else:
            reasoning.append("Sufficient confidence → using local RAG")

            response = format_response(
                query,
                local_data,
                "Local RAG",
                confidence,
                reasoning
            )

        # ---------------------------
        # STATE 4: STORE HISTORY
        # ---------------------------
        self.history.append({
            "query": query,
            "response": response
        })

        return response