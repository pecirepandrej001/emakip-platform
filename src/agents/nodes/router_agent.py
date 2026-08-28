from src.agents.state import AgentState

def router_agent(state: AgentState) -> AgentState:
    question = state["question"].lower()
    if any(term in question for term in ("how many users", "how many documents", "conversation count", "statistics")):
        route = "sql"
    elif any(term in question for term in ("document", "contract", "policy", "knowledge", "uploaded", "according to")):
        route = "rag"
    else:
        route = "rag"
    steps = state.get("steps", []) + [{"agent": "router", "status": f"selected:{route}"}]
    return {"route": route, "steps": steps}
