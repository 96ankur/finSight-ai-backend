from .calculator import CalculatorTool
from .financial_metrics import FinancialMetricsTool
from .document_search import DocumentSearchTool
from ..rag.retriever import get_user_retriever


class ToolRegistry:

    def __init__(self, retriever):
        self.tools = {
            "document_search": DocumentSearchTool(retriever),
            "calculator": CalculatorTool(),
            "financial_metrics": FinancialMetricsTool(),
        }

    @classmethod
    def for_user(self, user_id):
        retriever = get_user_retriever(user_id)
        return self(retriever)

    def get_tool(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return self.tools
