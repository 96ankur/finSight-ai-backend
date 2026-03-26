from typing import AsyncGenerator
from pydantic import BaseModel
from typing import Literal
from ..prompts.system import SYSTEM_PROMPT
from abc import ABC, abstractmethod
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

Role = Literal["system", "user", "assistant"]

class ChatMessage(BaseModel):
    role: Role
    content: str

def build_prompt(history: list[ChatMessage], user_message: str) -> list[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history, {"role": "user", "content": user_message}]
    return messages

class BaseLLMClient():
    @abstractmethod
    async def stream(
        self,
        messages: list[dict]
    ) -> AsyncGenerator[str, None]:
        pass

class GroqLLMClient(BaseLLMClient):
    def __init__(self, api_key: str, model: str):
        self.llm = ChatGroq(groq_api_key=api_key, model_name=model, streaming=True)

    def _to_langchain_messages(self, messages: list[dict]):
        """Convert OpenAI-style messages to LangChain messages."""
        lc_messages = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "user":
                lc_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))

        return lc_messages

    async def stream(self, messages) -> AsyncGenerator[str, None]:
        lc_messages = self._to_langchain_messages(messages)
        async for chunk in self.llm.astream(lc_messages):
            if chunk.content:
                yield chunk.content

async def single_agent_chat_bot_native_code(llm: BaseLLMClient, history: list[ChatMessage], user_message:str) -> AsyncGenerator[str, None]:
    prompt = build_prompt(history, user_message)
    assistant_message = ""

    async for token in llm.stream(prompt):
        assistant_message += token
        yield token

    history.append(ChatMessage(role="user", content=user_message))
    history.append(ChatMessage(role="assistant", content=assistant_message))


_conversations: dict[str, list[ChatMessage]] = {}

def get_conversation(conversation_id: str) -> list[ChatMessage]:
    return _conversations.setdefault(conversation_id, [])