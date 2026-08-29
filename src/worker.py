import asyncio
import uuid
from pathlib import Path
from celery import Celery
from sqlalchemy import select
from src.core.config import get_settings
from src.core.database import SessionLocal
from src.db.models.document import Document
from src.rag.chunking.recursive_chunker import recursive_chunk
from src.rag.embeddings.hf_embeddings import embed_texts
from src.rag.loaders.docx_loader import load_docx
from src.rag.loaders.pdf_loader import load_pdf
from src.rag.vector_store.qdrant_client import QdrantVectorStore

settings = get_settings()
celery_app = Celery("emakip", broker=settings.redis_url, backend=settings.redis_url)

def _load_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return load_pdf(path)
    if path.suffix.lower() == ".docx":
        return load_docx(path)
    return path.read_text(encoding="utf-8", errors="ignore")

async def _ingest(document_id: int) -> None:
    async with SessionLocal() as session:
        doc = await session.get(Document, document_id)
        if not doc:
            return
        try:
            doc.status = "processing"
            await session.commit()
            text = _load_text(Path(doc.storage_path))
            chunks = recursive_chunk(text, settings.chunk_size, settings.chunk_overlap)
            vectors = embed_texts(chunks) if chunks else []
            points = []
            for idx, (chunk, vector) in enumerate(zip(chunks, vectors, strict=True)):
                points.append({
                    "id": str(uuid.uuid5(uuid.NAMESPACE_URL, f"emakip:{document_id}:{idx}")),
                    "vector": vector,
                    "payload": {
                        "document_id": document_id,
                        "chunk_index": idx,
                        "filename": doc.filename,
                        "text": chunk,
                        "owner_email": doc.owner_email,
                    },
                })
            if points:
                await QdrantVectorStore().upsert(points)
            doc.chunk_count = len(chunks)
            doc.status = "ready"
            doc.error_message = None
        except Exception as exc:
            doc.status = "failed"
            doc.error_message = str(exc)[:2000]
        await session.commit()

@celery_app.task(name="ingest_document")
def ingest_document_task(document_id: int) -> None:
    asyncio.run(_ingest(document_id))
