from app.rag.embeddings import embed_text
from app.rag.chroma_client import get_chroma_client
from app.config import COLLECTION_NAME

def retrieve_context(question: str, top_k: int = 5) -> str:
    """
    1. Embed the question
    2. Query ChromaDB with the embedding
    3. Return joined documents
    """

    # ✅ STEP 1: Convert text → embedding
    query_embedding = embed_text(question)

    # ✅ STEP 2: Query ChromaDB with VECTOR
    client = get_chroma_client()
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.query(
        query_embeddings=[query_embedding],  # ✅ LIST[float]
        n_results=top_k
    )

    documents = results["documents"][0]

    # ✅ STEP 3: Return STRING (not list)
    return "\n\n".join(documents)
