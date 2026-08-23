from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.models.base import Base, TimestampMixin

class Document(TimestampMixin, Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), index=True)
    content_type: Mapped[str] = mapped_column(String(100), default="application/octet-stream")
    storage_path: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="queued")
    chunk_count: Mapped[int] = mapped_column(default=0)
    owner_email: Mapped[str] = mapped_column(String(320), index=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
