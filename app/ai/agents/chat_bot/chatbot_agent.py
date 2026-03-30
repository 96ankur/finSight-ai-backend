from typing import AsyncGenerator
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from ...prompts.system import SYSTEM_PROMPT
from ...prompts.agent_prompt import agent_prompt
from app.utils.agent_util import parse_agent_output
from ...tools.tool_registry import ToolRegistry
from app.core.logging import get_logger

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

    # What is the need for a memory store? Can't we get the history every time from ConversationBufferMemory?
    # Ans: ConversationBufferMemory is NOT global memory. It stores history only for one conversation instance.
    def _get_memory(self, conversation_id: str):
        if conversation_id not in self.memory_store:
            self.memory_store[conversation_id] = ChatMessageHistory()
        return self.memory_store[conversation_id]

    """
    RunnableWithMessageHistory is not required in this approach
     - Now your system is:
        loop:
            LLM → tool → LLM → tool → LLM

    This breaks the abstraction of RunnableWithMessageHistory because:
    - Problem 1: Multiple LLM Calls
        That wrapper assumes one LLM call per request, but now you have many.
    - Problem 2: You Control Messages Manually
        You are doing: messages.append(...)
        So, You already are the memory manager now.
    - Problem 3: Tool Interactions Are Invisible to It
        RunnableWithMessageHistory doesn't know:
         - when tools are called
         - what tool returned
         - how to inject tool outputs 
    
    """

    async def stream(self, conversation_id: str, user_message: str, user_id: str):

        memory = self._get_memory(conversation_id)
        messages = memory.messages.copy()

        registry = ToolRegistry.for_user(user_id)

        MAX_STEPS = 3  # prevent infinite loops

        last_tool = None
        last_tool_input = None
        last_tool_result = None

        for step in range(MAX_STEPS):
            logger.info(f"--- STEP {step} START ---")

            # STEP 1: Agent Decision
            decision_chain = agent_prompt | self.llm
            logger.info(f"messages: ", messages)
            # break
            decision = await decision_chain.ainvoke(
                {"input": f"{user_message}\n\nThink step by step. Do you need to use a tool?", "history": messages}
            )

            logger.info(f"Decision: {decision.content}")

            parsed = parse_agent_output(decision.content)

            logger.info(f"Parsed: {parsed}")

            tool_name = parsed.get("tool")
            tool_input = parsed.get("input", "")

            logger.info(f"Tool Name: {tool_name}")
            logger.info(f"Tool Input: {tool_input}")

            # Termination condition incase agent stuck in loop
            if tool_name == last_tool and tool_input == last_tool_input:
                yield f"Final Answer: {last_tool_result}"
                return

            last_tool = tool_name
            last_tool_input = tool_input

            logger.info("Tool Input:", tool_input)

            if tool_name == "document_search":
                tool_input["user_id"] = user_id

            print(f"[STEP {step}] Tool Name:{tool_name}, Tool Input: {tool_input}")

            # FINAL ANSWER (no tool)
            if not tool_name or tool_name == "none":
                final_answer = parsed.get("answer", decision.content)

                # stream final answer
                for char in final_answer:
                    yield char

                memory.add_user_message(user_message)
                memory.add_ai_message(final_answer)
                return

            # TOOL EXECUTION
            tool_entry = registry.get_tool(tool_name)

            if not tool_entry:
                yield f"Tool {tool_name} not found"
                return

            tool = tool_entry["tool"]
            input_model = tool_entry["input_model"]

            # error handling if tool execution fails
            try:
                if not isinstance(tool_input, dict):
                    messages.append(
                        HumanMessage(
                            content=f"""
                                Invalid input format for tool {tool_name}.

                                Expected JSON object but got:
                                {tool_input}

                                Fix and retry.
                            """
                        )
                    )
                    continue

                structured_input = input_model(**tool_input)
                tool_output = tool.run(structured_input)

                tool_result = tool_output.result

                last_tool_result = tool_result

                logger.info(f"Tool Result: {tool_result}")

            except Exception as e:
                tool_result = f"ERROR: {str(e)}"

                messages.append(
                    HumanMessage(
                        content=f"""
                            Tool {tool_name} failed.

                            Error:
                            {str(e)}

                            Fix your input and try again.
                        """
                    )
                )

                continue

            # CRITICAL: Feed tool result back into conversation
            messages.append(
                HumanMessage(
                    content=f"""
            You used tool: {tool_name}

            Tool result:
            {tool_result}

            Now perform the following steps:

            1. Extract all relevant numerical values
            2. Convert them into structured JSON format like:
            {{
                "current": number,
                "previous": number
            }}

            3. Decide:
            - If calculation is needed → call financial_metrics
            - Otherwise → return final answer

            IMPORTANT:
            - Do NOT pass raw text to tools
            - ONLY pass structured numerical values
            """
                )
            )

        # fallback if loop ends
        yield "Sorry, I couldn't complete the request."

    # ****************** OLD version of the steam with single tool calling and RunnableWithMessageHistory *******************************

    # async def stream(self, conversation_id: str, user_message: str, user_id: str) -> AsyncGenerator[str, None]:

    #     memory = self._get_memory(conversation_id)

    #     # STEP 1: Agent Decision (Non-streaming, fast)
    #     decision_chain = agent_prompt | self.llm

    #     decision = await decision_chain.ainvoke({"input": user_message, "history": memory.messages})

    #     parsed = parse_agent_output(decision.content)
    #     tool_name = parsed.get("tool")
    #     tool_input = parsed.get("input", user_message)
    #     print("toolt name: ", tool_name)
    #     context = ""
    #     # STEP 2: If RAG → fetch context and Build dynamic prompt
    #     if tool_name:
    #         registry = ToolRegistry(user_id)
    #         tool = registry.get_tool(tool_name)

    #         if tool:
    #             context = tool.run(tool_input)

    #     if context:
    #         prompt = ChatPromptTemplate.from_messages(
    #             [
    #                 ("system", SYSTEM_PROMPT + "\nUse the provided context."),
    #                 MessagesPlaceholder(variable_name="history"),
    #                 ("human", "Context:\n" + context + "\n\nQuestion:\n" + user_message),
    #             ]
    #         )

    #         self.chain = prompt | self.llm

    #     # NORMAL CHAT (your existing flow)
    #     runnable = RunnableWithMessageHistory(
    #         self.chain,
    #         lambda _: memory,
    #         input_messages_key="input",
    #         history_messages_key="history",
    #     )

    #     async for chunk in runnable.astream(
    #         {"input": user_message}, config={"configurable": {"session_id": conversation_id}}
    #     ):
    #         if chunk.content:
    #             yield chunk.content
