import asyncio
from src.core.database import SessionLocal, init_db
from src.core.security import hash_password
from src.db.repositories.user_repository import UserRepository

async def main():
    await init_db()
    async with SessionLocal() as session:
        repo = UserRepository(session)
        email = "admin@emakip.local"
        if not await repo.get_by_email(email):
            await repo.create(email=email, full_name="EMAKIP Admin",
                              hashed_password=hash_password("Admin123!"), role="admin")
            print("Created demo admin: admin@emakip.local / Admin123!")
        else:
            print("Demo admin already exists.")

if __name__ == "__main__":
    asyncio.run(main())
