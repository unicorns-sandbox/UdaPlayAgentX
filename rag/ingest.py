import json
from rag.vector_store import VectorStoreManager

def load_and_ingest():
    with open("data/games.json") as f:
        games = json.load(f)

    docs = []
    for g in games:
        text = f"""
        Title: {g['title']}
        Developer: {g['developer']}
        Release: {g['release_date']}
        Platform: {g['platform']}
        Genre: {g['genre']}
        """
        docs.append(text)

    db = VectorStoreManager()
    db.add_documents(docs)

    return db