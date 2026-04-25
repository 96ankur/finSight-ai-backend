from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from app.schemas import chat as ChatSchema
from app.services import chat_service
router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/stream")
async def chat(message: ChatSchema.ChatRequest):
    response = await chat_service.start_chat(message)

    return response
