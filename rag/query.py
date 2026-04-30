from rag.ingest import load_and_ingest

db = load_and_ingest()

def semantic_search(query):
    results = db.query(query)
    return results["documents"]