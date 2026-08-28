from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

ALLOWED_QUERIES = {
    "document_count": "SELECT COUNT(*) AS value FROM documents",
    "conversation_count": "SELECT COUNT(*) AS value FROM conversations",
    "user_count": "SELECT COUNT(*) AS value FROM users",
}

async def run_safe_analytics(session: AsyncSession, metric: str) -> int:
    if metric not in ALLOWED_QUERIES:
        raise ValueError("Unsupported analytics metric")
    result = await session.execute(text(ALLOWED_QUERIES[metric]))
    return int(result.scalar_one())
