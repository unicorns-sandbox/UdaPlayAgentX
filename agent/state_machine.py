class AgentStateMachine:

    def run(self, query, retrieve, evaluate, web_search):

        state = "START"
        reasoning = []

        # STATE 1: RETRIEVE
        if state == "START":
            result = retrieve(query)
            reasoning.append("Used retrieve_game")
            state = "EVALUATE"

        # STATE 2: EVALUATE
        if state == "EVALUATE":
            score = evaluate(result)
            reasoning.append(f"Score: {score}")

            if score < 0.6:
                state = "WEB"
            else:
                state = "END"

        # STATE 3: WEB FALLBACK
        if state == "WEB":
            result = web_search(query)
            reasoning.append("Used web search")
            state = "END"

        return result, reasoning