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
documents = [
  
    "địt nhau rất là vui",
    "mút buồi sướng lồn",
]

embeds = embedding_func(documents)

metadatas = [
    {"topic": "fuck"},
    {"topic": "fuck"}
]

ids = ["doc4", "doc5"]

collection.add(
    documents=documents,
    embeddings=embeds,
    metadatas=metadatas,
    ids=ids
)
