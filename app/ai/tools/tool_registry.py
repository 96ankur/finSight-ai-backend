from .calculator import CalculatorTool, CalculatorInput
from .financial_metrics import FinancialMetricsTool, FinancialInput
from .document_search import DocumentSearchTool, DocumentSearchInput
from ..rag.retriever import get_user_retriever


class ToolRegistry:

    def __init__(self, retriever):
        self.tools = {
            "document_search": {
                "tool": DocumentSearchTool(retriever),
                "input_model": DocumentSearchInput
            },
            "calculator": {
                "tool": CalculatorTool(),
                "input_model": CalculatorInput
            },
            "financial_metrics": {
                "tool": FinancialMetricsTool(),
                "input_model": FinancialInput
            },
        }

    @classmethod
    def for_user(self, user_id):
        retriever = get_user_retriever(user_id)
        return self(retriever)

    def get_tool(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return self.tools
