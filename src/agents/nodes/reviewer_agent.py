from src.agents.state import AgentState

def reviewer_agent(state: AgentState) -> AgentState:
    evidence = state.get("evidence", [])
    confidence = 0.9 if evidence else 0.35
    status = "grounded" if evidence else "insufficient_evidence"
    return {
        "confidence": confidence,
        "steps": state.get("steps", []) + [{"agent": "reviewer", "status": status}],
    }
