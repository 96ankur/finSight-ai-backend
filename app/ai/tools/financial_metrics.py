from .base import BaseTool, ToolInput, ToolOutput


class FinancialInput(ToolInput):
    metric: str
    current: float
    previous: float


class FinancialMetricsTool(BaseTool):
    name = "financial_metrics"
    description = "Calculates financial metrics like growth"

    def run(self, input: FinancialInput) -> ToolOutput:
        if input.metric == "growth":
            growth = ((input.current - input.previous) / input.previous) * 100

            return ToolOutput(
                result=f"{growth:.2f}%",
                metadata={
                    "current": input.current,
                    "previous": input.previous
                }
            )

        return ToolOutput(result="Unknown metric")