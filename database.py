import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="study_notes")

def add_chunk(chunk_id: str, text: str, embedding: list[float], metadata: dict):
    collection.add(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
    )

def query(embedding: list[float], k: int = 4):
    return collection.query(query_embeddings=[embedding], n_results=k)