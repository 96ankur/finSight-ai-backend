from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from app.schemas import chat as ChatSchema
from app.services import chat_service
router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/stream")
async def chat(message: ChatSchema.ChatRequest):
    event_generator = await chat_service.stream_chat(message)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
