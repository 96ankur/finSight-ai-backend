from ...rag.pipeline import run_rag

class RAGTool:

    name = "document_search"
    description = "Search and answer from user uploaded documents"

    def __init__(self, user_id: str, llm):
        self.user_id = user_id
        self.llm = llm

    def run(self, query: str):
        return run_rag(query, self.user_id, self.llm)