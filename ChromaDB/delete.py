import chromadb

client = chromadb.PersistentClient(path="./chroma_store")
# Tạo hoặc lấy collection
collection = client.get_or_create_collection(name="demo_vectors")

collection.delete(ids=["doc2"])