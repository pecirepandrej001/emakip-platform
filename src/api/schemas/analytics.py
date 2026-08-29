from pydantic import BaseModel

class AnalyticsResponse(BaseModel):
    users: int
    documents: int
    conversations: int
