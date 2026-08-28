from typing import TypedDict

class AgentState(TypedDict, total=False):
    question: str
    user_email: str
    route: str
    evidence: list[dict]
    draft: str
    answer: str
    confidence: float
    steps: list[dict[str, str]]
