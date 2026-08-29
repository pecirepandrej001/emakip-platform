from fastapi import APIRouter, Depends
from src.api.dependencies import get_current_user
from src.db.models.user import User

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("/status")
async def agent_status(_: User = Depends(get_current_user)):
    return {
        "status": "ready",
        "agents": [
            {"name": "router", "status": "ready"},
            {"name": "document_analyzer", "status": "ready"},
            {"name": "sql_analytics", "status": "ready"},
            {"name": "reviewer", "status": "ready"},
            {"name": "summarizer", "status": "ready"},
        ],
    }
