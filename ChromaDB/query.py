import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path="./chroma_store")

model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=model_name
)

collection = client.get_or_create_collection(
    name="demo_vectors_vi"
)


query = "địt có vui không"
query_emb = embedding_func([query])

results = collection.query(
    query_embeddings=query_emb,
    n_results=2,
    include=["documents", "metadatas", "distances", "embeddings"]
)

print(results["documents"])
