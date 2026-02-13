import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "rag_documents"

USE_CHROMA_HTTP = os.getenv("USE_CHROMA_HTTP", "false").lower() == "true"
CHROMA_HOST = os.getenv("CHROMA_HOST", "127.0.0.1")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8001"))
