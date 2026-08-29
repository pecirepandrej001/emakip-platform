from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.dependencies import get_current_user
from src.api.schemas.analytics import AnalyticsResponse
from src.agents.tools.db_query_tool import run_safe_analytics
from src.core.database import get_db
from src.db.models.user import User

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("", response_model=AnalyticsResponse)
async def analytics(
    _: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return AnalyticsResponse(
        users=await run_safe_analytics(session, "user_count"),
        documents=await run_safe_analytics(session, "document_count"),
        conversations=await run_safe_analytics(session, "conversation_count"),
    )
