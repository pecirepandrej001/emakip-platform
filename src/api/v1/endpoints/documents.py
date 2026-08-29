from pathlib import Path
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.dependencies import get_current_user
from src.api.schemas.document import DocumentResponse
from src.core.database import get_db
from src.db.models.user import User
from src.db.repositories.document_repository import DocumentRepository
from src.worker import ingest_document_task
from src.rag.vector_store.qdrant_client import QdrantVectorStore

router = APIRouter(prefix="/documents", tags=["documents"])
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}

@router.post("", response_model=DocumentResponse, status_code=202)
async def upload_document(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Allowed file types: {sorted(ALLOWED_EXTENSIONS)}")
    filename = f"{uuid.uuid4().hex}{suffix}"
    path = UPLOAD_DIR / filename
    content = await file.read()
    if len(content) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Maximum upload size is 25 MB")
    path.write_bytes(content)

    doc = await DocumentRepository(session).create(
        filename=file.filename or filename,
        content_type=file.content_type or "application/octet-stream",
        storage_path=str(path),
        status="queued",
        owner_email=user.email,
    )
    ingest_document_task.delay(doc.id)
    return doc

@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await DocumentRepository(session).list_for_owner(user.email)

@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    repo = DocumentRepository(session)
    doc = await repo.get(document_id)
    if not doc or doc.owner_email != user.email:
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        await QdrantVectorStore().delete_document(document_id)
    except Exception:
        pass
    Path(doc.storage_path).unlink(missing_ok=True)
    await repo.delete(doc)
