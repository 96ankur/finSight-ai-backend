from typing import AsyncGenerator
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from ...prompts.system import SYSTEM_PROMPT
from ...prompts.agent_prompt import agent_prompt
from ...rag.retriever import get_user_retriever
from app.utils.agent_util import parse_agent_output
from ..tools.tool_registry import ToolRegistry

class Chatbot_agent:
    def __init__(self, api_key: str, model: str):
        self.llm = ChatGroq(
            api_key=api_key,
            model=model,
            streaming=True,
            temperature=0.2,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT), MessagesPlaceholder(variable_name="history"), ("human", "{input}")]
        )

        self.memory_store = {}

        self.chain = self.prompt | self.llm

    # What is the need for a memory store? Can't we get the history every time from ConversationBufferMemory?
    # Ans: ConversationBufferMemory is NOT global memory. It stores history only for one conversation instance.
    def _get_memory(self, conversation_id: str):
        if conversation_id not in self.memory_store:
            self.memory_store[conversation_id] = ChatMessageHistory()
        return self.memory_store[conversation_id]

    async def stream(self, conversation_id: str, user_message: str, user_id: str) -> AsyncGenerator[str, None]:

        memory = self._get_memory(conversation_id)

        # STEP 1: Agent Decision (Non-streaming, fast)
        decision_chain = agent_prompt | self.llm

        decision = await decision_chain.ainvoke({"input": user_message, "history": memory.messages})

        parsed = parse_agent_output(decision.content)
        tool_name = parsed.get("tool")
        tool_input = parsed.get("input", user_message)
        print("toolt name: ", tool_name)
        context = ""
        # STEP 2: If RAG → fetch context and Build dynamic prompt
        if tool_name:
            registry = ToolRegistry(user_id, self.llm)
            tool = registry.get_tool(tool_name)

            if tool:
                context = tool.run(tool_input)
        
        if context:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", SYSTEM_PROMPT + "\nUse the provided context."),
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "Context:\n" + context + "\n\nQuestion:\n" + user_message),
                ]
            )

            self.chain = prompt | self.llm

        # NORMAL CHAT (your existing flow)
        runnable = RunnableWithMessageHistory(
            self.chain,
            lambda _: memory,
            input_messages_key="input",
            history_messages_key="history",
        )

        async for chunk in runnable.astream(
            {"input": user_message}, config={"configurable": {"session_id": conversation_id}}
        ):
            if chunk.content:
                yield chunk.content
