from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import chat
from app.api.v1.endpoints import rag

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(chat.router)
api_router.include_router(rag.router)

