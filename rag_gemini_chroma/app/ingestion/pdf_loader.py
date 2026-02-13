from pypdf import PdfReader

def load_and_split_pdf(file_path: str, chunk_size: int = 500, overlap: int = 50):
    """
    Load a PDF and split text into overlapping chunks
    """

    reader = PdfReader(file_path)
    full_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # -------------------------
    # Split into chunks
    # -------------------------
    chunks = []
    start = 0

    while start < len(full_text):
        end = start + chunk_size
        chunks.append(full_text[start:end])
        start = end - overlap

    return chunks
