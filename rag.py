import json

def retrieve_local(query):
    with open("data/games.json") as f:
        games = json.load(f)

    query = query.lower()

    results = []
    for game in games:
        if query in game["title"].lower():
            results.append(game)

    return results