import json
import os
from vector_store import VectorStoreManager


def load_games(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_game(game):
    return (
        f"{game.get('title')} is a {game.get('genre')} game "
        f"developed by {game.get('developer')} "
        f"released in {game.get('release_date')} "
        f"available on {game.get('platform')}."
    )


def ingest_games():
    vs = VectorStoreManager()

    vs.reset_collection()

    data_path = os.path.join("data", "games.json")
    games = load_games(data_path)

    ids = []
    documents = []
    metadatas = []

    for game in games:
        game_id = str(game.get("id"))
        text = format_game(game)

        ids.append(game_id)
        documents.append(text)
        metadatas.append({
            "title": game.get("title"),
            "genre": game.get("genre"),
            "developer": game.get("developer"),
            "platform": game.get("platform"),
            "release_date": game.get("release_date"),
        })

    vs.add_documents(ids, documents, metadatas)

    print(f"Ingested {len(ids)} games.")


if __name__ == "__main__":
    ingest_games()
