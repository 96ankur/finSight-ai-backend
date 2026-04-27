from typing import AsyncGenerator
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from ..prompts.system import SYSTEM_PROMPT
from ..prompts.agent_prompt import agent_prompt
from app.utils.parsing.output_parser import parse_agent_output
from ..tools.tool_registry import ToolRegistry
from app.core.logging import get_logger
from ..tools.tool_executor import ToolExecutor
from ...utils.retry import get_valid_decision
from .orchestrator_agent import Orchestrator

logger = get_logger("access")


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

    async def stream(self, user_message: str, user_id: str):
        orchestrator = Orchestrator(self.llm)

        response = await orchestrator.run(
            query=user_message,
            user_id=user_id
        )
        yield response