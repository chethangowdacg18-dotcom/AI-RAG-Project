from app.rag.chroma_client import get_chroma_client
from app.config import COLLECTION_NAME

def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

def add_documents(ids, documents, embeddings, metadatas):
    collection = get_collection()
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def query_vectors(query_embedding, top_k=5):
    collection = get_collection()
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

def get_collection_stats():
    collection = get_collection()
    return {
        "count": collection.count()
    }

def peek_documents(limit=5):
    collection = get_collection()
    return collection.peek(limit=limit)
