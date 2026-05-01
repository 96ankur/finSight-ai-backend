# from .calculator import CalculatorTool, CalculatorInput
# from .financial_metrics import FinancialMetricsTool, FinancialInput

# class ToolRegistry:

#     def __init__(self, retriever):
#         self.tools = {
#             # "document_search": {
#             #     "tool": DocumentSearchTool(retriever),
#             #     "input_model": DocumentSearchInput
#             # },
#             "calculator": {
#                 "tool": CalculatorTool(),
#                 "input_model": CalculatorInput
#             },
#             "financial_metrics": {
#                 "tool": FinancialMetricsTool(),
#                 "input_model": FinancialInput
#             },
#         }

#     # @classmethod
#     # def for_user(self, user_id):
#     #     retriever = get_user_retriever(user_id)
#     #     return self(retriever)

#     def get_tool(self, name: str):
#         return self.tools.get(name)

#     def list_tools(self):
#         return self.tools
    
#     def get_tool_descriptions():
#         return 


from typing import Dict


class Tool:
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self.func = func


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def get_all_tools(self):
        return list(self.tools.values())

    def get_tool(self, name: str):
        return self.tools.get(name)
    
    def get_tool_descriptions(self):
        return ",".join([tool.description for tool in list(self.tools.values)])