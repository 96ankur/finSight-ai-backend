# from app.ai.chat_bot.single_agent_chatbot_native_code import get_conversation, GroqLLMClient, single_agent_chat_bot
# from app.schemas import chat as ChatSchema
# async def stream_chat(message: ChatSchema.ChatRequest):
#     history = get_conversation(message.conversation_id)

#     llm_client = GroqLLMClient(message.api_key, message.model)

#     async def event_generator():
#         async for token in single_agent_chat_bot_native_code(
#             llm=llm_client,
#             history=history,
#             user_message=message.message
#         ):
#             yield f"data: {token}\n\n"

#     return event_generator
    

# from app.ai.agents.chat_bot.single_agent_chatbot import SingleAgentLangChainChatbot
from app.ai.agents.chat_bot.chatbot_agent import Chatbot_agent

from app.schemas import chat as ChatSchema

async def stream_chat(message: ChatSchema.ChatRequest):
    # client = SingleAgentLangChainChatbot(message.api_key, message.model)
    client = Chatbot_agent(message.api_key, message.model)


    async def event_generator():
        async for token in client.stream(
            conversation_id=message.conversation_id,
            user_message=message.message,
            user_id=message.user_id
        ):
            yield f"data: {token}\n\n"

    return event_generator