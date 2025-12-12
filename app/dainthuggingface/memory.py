import chromadb
from chromadb.utils import embedding_functions

class MemoryStore:
    def __init__(self, path="./daint_chat_chroma_store"):
        self.client = chromadb.PersistentClient(path=path)

        self.embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.collection = self.client.get_or_create_collection(
            name="chat_history_vi"
        )

    def add_message(self, role, content):
        emb = self.embedder([content])
        self.collection.add(
            documents=[content],
            embeddings=emb,
            metadatas=[{"role": role}],
            ids=[f"msg_{self.collection.count()}"]
        )

    def query(self, text, k=3):
        q_emb = self.embedder([text])
        results = self.collection.query(
            query_embeddings=q_emb,
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        return results["documents"][0] if results["documents"] else []