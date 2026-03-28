from abc import ABC, abstractmethod
from pydantic import BaseModel


class ToolInput(BaseModel):
    pass


class ToolOutput(BaseModel):
    result: str
    metadata: dict = {}


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, input: ToolInput) -> ToolOutput:
        pass