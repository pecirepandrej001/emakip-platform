from src.agents.state import AgentState
from src.core.config import get_settings

async def summarizer_agent(state: AgentState) -> AgentState:
    settings = get_settings()
    draft = state.get("draft", "")
    evidence = state.get("evidence", [])

    if settings.openai_api_key and evidence:
        try:
            from langchain_openai import ChatOpenAI
            model = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0)
            context = "\n\n".join(f"- {e['filename']}: {e['text']}" for e in evidence)
            prompt = (
                "Answer the question using only the supplied evidence. "
                "If evidence is incomplete, say so. Be concise.\n\n"
                f"Question: {state['question']}\n\nEvidence:\n{context}"
            )
            response = await model.ainvoke(prompt)
            answer = str(response.content)
        except Exception:
            answer = _local_answer(state["question"], evidence, draft)
    else:
        answer = _local_answer(state["question"], evidence, draft)

    return {
        "answer": answer,
        "steps": state.get("steps", []) + [{"agent": "summarizer", "status": "completed"}],
    }

def _local_answer(question: str, evidence: list[dict], draft: str) -> str:
    if not evidence:
        return "I could not find enough indexed evidence to answer that reliably."
    if len(evidence) == 1 and evidence[0].get("filename") == "platform_database":
        return draft
    snippets = "\n".join(f"- {e['text'][:420]}" for e in evidence[:4])
    return f"Based on the indexed knowledge base:\n{snippets}"
