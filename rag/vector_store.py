import chromadb
from chromadb.utils import embedding_functions

class VectorStoreManager:
    def __init__(self):
        self.client = chromadb.Client()
        self.embedding = embedding_functions.DefaultEmbeddingFunction()

        self.collection = self.client.get_or_create_collection(
            name="games",
            embedding_function=self.embedding
        )

    def add_documents(self, docs):
        for i, doc in enumerate(docs):
            self.collection.add(
                documents=[doc],
                ids=[str(i)]
            )

    def query(self, query, n_results=2):
        return self.collection.query(
            query_texts=[query],
            n_results=n_results
        )