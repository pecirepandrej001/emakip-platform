from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)

class AgentStep(BaseModel):
    agent: str
    status: str

class SourceItem(BaseModel):
    filename: str
    text: str

class ChatResponse(BaseModel):
    answer: str
    route: str
    confidence: float
    steps: list[AgentStep]
    sources: list[SourceItem]
