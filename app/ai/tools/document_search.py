from .base import BaseTool, ToolInput, ToolOutput


class DocumentSearchInput(ToolInput):
    query: str
    user_id: str


class DocumentSearchTool(BaseTool):
    name = "document_search"
    description = "Searches user uploaded documents"

    def __init__(self, retriever):
        self.retriever = retriever

    def run(self, input: DocumentSearchInput) -> ToolOutput:
        docs = self.retriever.get_relevant_documents(
            query=input.query,
            user_id=input.user_id
        )

        content = "\n".join([doc.page_content for doc in docs])

        return ToolOutput(
            result=content,
            metadata={"num_docs": len(docs)}
        )