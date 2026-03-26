from .rag_tool import RAGTool

class ToolRegistry:

    def __init__(self, user_id: str, llm):
        self.tools = {
            "document_search": RAGTool(user_id, llm),
        }

    def get_tool(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return self.tools