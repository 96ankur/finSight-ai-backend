from pydantic import BaseModel
from typing import Optional, Dict

class AgentDecision(BaseModel):
    thought: str
    tool: Optional[str]
    input: Optional[Dict]
    answer: Optional[str]