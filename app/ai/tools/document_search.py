from .base import BaseTool, ToolInput, ToolOutput


class DocumentSearchInput(ToolInput):
    query: str
    user_id: str


class DocumentSearchTool(BaseTool):
    name = "document_search"
    description = "Searches user uploaded documents"

    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, query: str) -> ToolOutput:
        docs = self.retriever.invoke(query)

        content = "\n".join([doc.page_content for doc in docs])

        return ToolOutput(result=content, metadata={"num_docs": len(docs)})
