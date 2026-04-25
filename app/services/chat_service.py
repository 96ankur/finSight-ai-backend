from app.ai.agents.langgraph_agent import run_agent
from langchain_groq import ChatGroq
from app.schemas import chat as ChatSchema

async def start_chat(data: ChatSchema.ChatRequest):
    llm = ChatGroq(
        api_key=data.api_key,
        model=data.model,
        streaming=True,
        temperature=0.2,
    )
    response = await run_agent(llm, data.user_id, data.message)

    return response