import chromadb

client = chromadb.PersistentClient(path="./chroma_store")
# Tạo hoặc lấy collection
collection = client.get_or_create_collection(name="demo_vectors")

collection.update(
    ids=["doc2"],
    documents=["Hôm nay tôi ở nhà đọc sách thay vì đi dạo."]
)
