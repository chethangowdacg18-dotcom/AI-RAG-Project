import os
import shutil
import traceback

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.config import COLLECTION_NAME
from app.ingestion.ingest import ingest_pdf
from app.ingestion.pdf_loader import load_and_split_pdf
from app.rag.chroma_client import get_chroma_client
from app.rag.pipeline import rag_pipeline
from app.rag.vectorstore import get_collection

app = FastAPI()


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        text_chunks = load_and_split_pdf(file_path)
        ingest_pdf(text_chunks=text_chunks, source=file.filename)

        return {
            "status": "PDF ingested successfully",
            "source": file.filename,
            "chunks_ingested": len(text_chunks),
        }

    except Exception as e:
        print("PDF upload error")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.post("/query")
async def query_rag(question: str):
    try:
        answer = rag_pipeline(question)
        return {"answer": answer}
    except Exception as e:
        print("Query error")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chroma/summary")
async def chroma_summary(limit: int = 20):
    try:
        safe_limit = max(1, min(limit, 200))

        collection = get_collection()
        count = collection.count()
        records = collection.get(include=["documents", "metadatas"])

        ids = records.get("ids", [])
        documents = records.get("documents", [])
        metadatas = records.get("metadatas", [])

        sources = sorted(
            {
                md.get("source", "unknown")
                for md in metadatas
                if isinstance(md, dict)
            }
        )

        preview_rows = []
        total_chars = 0
        for idx, doc in enumerate(documents):
            text = doc or ""
            total_chars += len(text)

            source = "unknown"
            if idx < len(metadatas) and isinstance(metadatas[idx], dict):
                source = metadatas[idx].get("source", "unknown")

            preview_rows.append(
                {
                    "id": ids[idx] if idx < len(ids) else f"row-{idx}",
                    "source": source,
                    "chars": len(text),
                    "preview": text[:240],
                }
            )

        avg_chunk_chars = (total_chars / len(documents)) if documents else 0.0

        return {
            "collection_name": COLLECTION_NAME,
            "vector_count": count,
            "source_count": len(sources),
            "sources": sources,
            "avg_chunk_chars": round(avg_chunk_chars, 2),
            "preview_rows": preview_rows[:safe_limit],
        }
    except Exception as e:
        print("Chroma summary error")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chroma/clear")
async def clear_chroma():
    try:
        client = get_chroma_client()
        client.delete_collection(COLLECTION_NAME)
        client.get_or_create_collection(COLLECTION_NAME)
        return {"status": "cleared", "collection_name": COLLECTION_NAME}
    except Exception as e:
        print("Chroma clear error")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
