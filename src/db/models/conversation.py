from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.models.base import Base, TimestampMixin

class Conversation(TimestampMixin, Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_email: Mapped[str] = mapped_column(String(320), index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    route: Mapped[str] = mapped_column(String(50))
