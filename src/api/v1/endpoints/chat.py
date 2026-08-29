from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.graph import run_agent
from src.api.dependencies import get_current_user
from src.api.schemas.chat import AgentStep, ChatRequest, ChatResponse, SourceItem
from src.core.database import get_db
from src.core.telemetry import AGENT_RUNS
from src.db.models.user import User
from src.db.repositories.conversation_repository import ConversationRepository

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    state = await run_agent(payload.message, user.email)
    route = state.get("route", "unknown")
    AGENT_RUNS.labels(route=route).inc()
    answer = state.get("answer", "No answer generated.")
    await ConversationRepository(session).create(user.email, payload.message, answer, route)
    return ChatResponse(
        answer=answer,
        route=route,
        confidence=float(state.get("confidence", 0.0)),
        steps=[AgentStep(**s) for s in state.get("steps", [])],
        sources=[SourceItem(filename=e.get("filename","unknown"), text=e.get("text","")) for e in state.get("evidence",[])],
    )
