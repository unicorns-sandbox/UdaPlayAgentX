from rag.vector_store import VectorStoreManager


def search_games(query):
    vs = VectorStoreManager()
    results = vs.query(query, n_results=5)

    output = []

    for i in range(len(results["documents"][0])):
        metadata = results["metadatas"][0][i]

        output.append({
            "title": metadata["title"],
            "genre": metadata["genre"],
            "developer": metadata["developer"],
            "platform": metadata["platform"],
            "release_date": metadata["release_date"],
        })

    return output
