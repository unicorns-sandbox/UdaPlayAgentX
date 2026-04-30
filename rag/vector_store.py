import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


class VectorStoreManager:
    def __init__(self, collection_name="games", persist_dir="./chroma_db"):
        self.client = chromadb.Client(
            Settings(persist_directory=persist_dir)
        )

        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def embed(self, texts):
        return self.embedding_model.encode(texts).tolist()

    def add_documents(self, ids, documents, metadatas=None):
        embeddings = self.embed(documents)

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas if metadatas else [{} for _ in documents],
        )

    def query(self, query_text, n_results=5):
        query_embedding = self.embed([query_text])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    def persist(self):
        # Only needed if using older versions, but safe to include
        pass

    def reset_collection(self):
    self.client.delete_collection(name=self.collection.name)
    self.collection = self.client.get_or_create_collection(
        name=self.collection.name
    )
