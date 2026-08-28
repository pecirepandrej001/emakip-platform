from src.agents.state import AgentState
from src.core.database import SessionLocal
from src.agents.tools.db_query_tool import run_safe_analytics

async def sql_analytics_agent(state: AgentState) -> AgentState:
    q = state["question"].lower()
    metric = "conversation_count"
    if "user" in q:
        metric = "user_count"
    elif "document" in q:
        metric = "document_count"

    async with SessionLocal() as session:
        value = await run_safe_analytics(session, metric)
    return {
        "draft": f"{metric.replace('_', ' ').title()}: {value}",
        "evidence": [{"filename": "platform_database", "text": f"{metric}={value}"}],
        "steps": state.get("steps", []) + [{"agent": "sql_analytics", "status": f"metric:{metric}"}],
    }
