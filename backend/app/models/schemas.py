from pydantic import BaseModel
from typing import List, Literal, Optional

class ConversationInteraction(BaseModel):
    agentId: Literal["manager", "customer", "legal"]
    agentName: str
    text: str
    timeOffset: Optional[int] = 0

class PraxisResponse(BaseModel):
    riskScore: int
    riskLevel: Literal["low", "medium", "high"]
    sayDoGap: str
    insight: str
    saferVariant: str
    conversation: List[ConversationInteraction]

class PraxisRequest(BaseModel):
    prompt: str
