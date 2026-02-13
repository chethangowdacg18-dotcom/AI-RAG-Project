import chromadb
from app.config import CHROMA_DB_DIR, CHROMA_HOST, CHROMA_PORT, USE_CHROMA_HTTP


def get_chroma_client():
    """
    Connect to ChromaDB in either persistent local mode or HTTP server mode.
    """
    if USE_CHROMA_HTTP:
        return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)
