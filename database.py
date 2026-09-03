#database.py

import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="study_notes")
number_of_chunks = 4

def add_chunk(chunk_id: str, text: str, embedding: list[float], metadata: dict):
    """Add chunks to the database using four parameters"""
    collection.add(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
    )


def query(prompt_embedding: list[float], k: int = number_of_chunks):
    """Return the k stored chunks whose embeddings are most similar to the given query embedding."""
    return collection.query(query_embeddings=[prompt_embedding], n_results=k)