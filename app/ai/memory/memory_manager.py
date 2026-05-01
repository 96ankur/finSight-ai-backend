from app.ai.memory.vector_memory import VectorMemory
from app.ai.memory.summary_memory import SummaryMemory


class MemoryManager:
    def __init__(self, llm):
        self.vector_memory = VectorMemory()
        self.summary_memory = SummaryMemory(llm)

    # Build context before LLM call
    async def build_context(self, user_id: str, query: str):

        vector_context = self.vector_memory.retrieve(
            user_id,
            query
        )

        summaries = self.summary_memory.get(user_id)

        return f"""
            Relevant Facts:
            {vector_context}

            Session Summary:
            {summaries["session_summary"]}
        """
            # User Summary:
            # {summaries["user_summary"]}

    # Update memory after response
    async def update_memory(
        self,
        user_id: str,
        user_query: str,
        final_answer: str
    ):

        # Add to vector memory
        # self.vector_memory.add_user_memory(user_id, f"User: {user_query}")
        # self.vector_memory.add_user_memory(user_id, f"Assistant: {final_answer}")

        self.vector_memory.add_session_memory(user_id, f"User: {user_query}")
        self.vector_memory.add_session_memory(user_id, f"Assistant: {final_answer}")

        # Update summary
        conversation = f"User: {user_query}\nAssistant: {final_answer}"
        await self.summary_memory.update(user_id, conversation)

    # 🔹 Cleanup session
    def clear_session(self, session_id: str):
        self.vector_memory.clear_session(session_id)
        self.summary_memory.clear_session(session_id)