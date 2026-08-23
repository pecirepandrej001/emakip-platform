from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from src.db.models.base import Base, TimestampMixin

class AuditLog(TimestampMixin, Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    actor: Mapped[str] = mapped_column(String(320), index=True)
    action: Mapped[str] = mapped_column(String(100), index=True)
    details: Mapped[dict] = mapped_column(JSON, default=dict)
