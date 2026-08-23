from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    async def create(self, email: str, full_name: str, hashed_password: str, role: str = "user") -> User:
        user = User(email=email.lower(), full_name=full_name, hashed_password=hashed_password, role=role)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
