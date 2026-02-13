from sentence_transformers import SentenceTransformer

# Free, fast, excellent for RAG
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> list:
    """
    Generate vector embedding for text (FREE, local).
    """
    return _model.encode(text).tolist()
