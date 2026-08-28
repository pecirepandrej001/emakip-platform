from src.agents.state import AgentState
from src.agents.tools.rag_search_tool import rag_search

async def document_analyzer(state: AgentState) -> AgentState:
    evidence = await rag_search(state["question"])
    if evidence:
        draft = "\n\n".join(
            f"[{i+1}] {item['filename']}: {item['text']}" for i, item in enumerate(evidence)
        )
    else:
        draft = "No indexed evidence was found for this question."
    return {
        "evidence": evidence,
        "draft": draft,
        "steps": state.get("steps", []) + [{"agent": "document_analyzer", "status": f"retrieved:{len(evidence)}"}],
    }
