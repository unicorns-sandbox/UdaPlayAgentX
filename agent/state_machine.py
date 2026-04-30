from agent.tools import (
    retrieve_game,
    evaluate_retrieval,
    game_web_search
)


class GameAgent:
    def run(self, query):
        report = {
            "query": query,
            "steps": []
        }

        # STEP 1 — Retrieve
        retrieval = retrieve_game(query)
        report["steps"].append(retrieval)

        # STEP 2 — Evaluate
        evaluation = evaluate_retrieval(retrieval["results"])
        report["steps"].append(evaluation)

        # STEP 3 — Decision
        if evaluation["status"] == "pass":
            report["final"] = {
                "source": "vector_db",
                "results": retrieval["results"]
            }
            return report

        # STEP 4 — Web fallback
        web = game_web_search(query)
        report["steps"].append(web)

        report["final"] = {
            "source": "web",
            "results": web["results"]
        }

        return report
