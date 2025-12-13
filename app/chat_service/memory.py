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
        print(f"Querying for: {text}")
        q_emb = self.embedder([text])
        results = self.collection.query(
            query_embeddings=q_emb,
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        print(f"Query results: {results}")
        return results["documents"][0] if results["documents"] else []

    def delete_message(self, msg_id):
        self.collection.delete(ids=[msg_id])
    
    def clear_memory(self):
        self.collection.delete()

    def get_all_messages(self):
        results = self.collection.get()
        return results
    
    def count_messages(self):
        return self.collection.count()

    def close(self):
        self.client.persist()
    
    def update_message(self, msg_id, new_content):
        emb = self.embedder([new_content])
        self.collection.update(
            ids=[msg_id],
            documents=[new_content],
            embeddings=emb
        )