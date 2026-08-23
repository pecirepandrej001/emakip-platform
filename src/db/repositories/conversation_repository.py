from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.conversation import Conversation

class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_email: str, question: str, answer: str, route: str) -> Conversation:
        item = Conversation(user_email=user_email, question=question, answer=answer, route=route)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def recent(self, user_email: str, limit: int = 20) -> list[Conversation]:
        result = await self.session.execute(
            select(Conversation)
            .where(Conversation.user_email == user_email)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
