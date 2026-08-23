from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.document import Document

class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Document:
        doc = Document(**kwargs)
        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)
        return doc

    async def list_for_owner(self, owner_email: str) -> list[Document]:
        result = await self.session.execute(
            select(Document).where(Document.owner_email == owner_email).order_by(Document.created_at.desc())
        )
        return list(result.scalars().all())

    async def get(self, document_id: int) -> Document | None:
        return await self.session.get(Document, document_id)

    async def delete(self, doc: Document) -> None:
        await self.session.delete(doc)
        await self.session.commit()
