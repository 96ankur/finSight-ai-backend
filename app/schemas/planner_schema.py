from pydantic import BaseModel, Field
from typing import List, Dict


class PlanStep(BaseModel):
    action: str = Field(..., description="Tool name to call")
    input: Dict = Field(default_factory=dict)


class Plan(BaseModel):
    steps: List[PlanStep]