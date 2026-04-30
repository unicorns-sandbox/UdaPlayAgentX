def print_report(report):
    print("\n============================")
    print("        AGENTX REPORT        ")
    print("============================")

    print(f"\nQuery: {report['query']}")

    for step in report["steps"]:
        print(f"\n--- {step['tool']} ---")

        if step["tool"] == "retrieve_game":
            for r in step["results"]:
                print(r)

        elif step["tool"] == "game_web_search":
            for r in step["results"]:
                print(f"- {r['title']}")
                print(f"  {r['content']}")
                print(f"  {r['url']}")

        else:
            for k, v in step.items():
                if k != "tool":
                    print(f"{k}: {v}")

    print("\n===== FINAL OUTPUT =====")
    print(f"Source: {report['final']['source']}")

    for r in report["final"]["results"]:
        print(r)
