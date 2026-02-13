import uuid
from app.rag.embeddings import embed_text
from app.rag.vectorstore import add_documents

def ingest_pdf(text_chunks: list[str], source: str):
    """
    Takes extracted PDF text chunks and stores them in ChromaDB
    """

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in text_chunks:
        ids.append(str(uuid.uuid4()))
        documents.append(chunk)
        embeddings.append(embed_text(chunk))  # ✅ VECTOR
        metadatas.append({"source": source})

    # ✅ THIS IS THE CRITICAL LINE
    add_documents(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
