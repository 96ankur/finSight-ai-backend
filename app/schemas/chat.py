from pydantic import BaseModel

class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    model: str
    api_key: str
    user_id: str