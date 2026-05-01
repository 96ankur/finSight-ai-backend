class SummaryMemory:
    def __init__(self, llm):
        self.llm = llm
        # self.user_summaries = {}
        self.session_summaries = {}

    async def update(self, user_id: str, conversation: str):

        prompt = f"""
            Summarize the following conversation concisely:

            {conversation}
        """

        response = await self.llm.ainvoke(prompt)
        summary = response.content

        # store both
        # self.user_summaries[user_id] = summary
        self.session_summaries[user_id] = summary

    def get(self, user_id: str):
        return {
            # "user_summary": self.user_summaries.get(user_id, ""),
            "session_summary": self.session_summaries.get(user_id, "")
        }

    def clear_session(self, session_id: str):
        if session_id in self.session_summaries:
            del self.session_summaries[session_id]