from .base import BaseTool, ToolInput, ToolOutput
from pydantic import BaseModel


class CalculatorInput(ToolInput):
    expression: str


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs mathematical calculations"

    def run(self, input: CalculatorInput) -> ToolOutput:
        try:
            result = eval(input.expression)
            return ToolOutput(result=str(result))
        except Exception as e:
            return ToolOutput(
                result="Error in calculation",
                metadata={"error": str(e)}
            )