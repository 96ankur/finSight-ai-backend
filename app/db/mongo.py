from __future__ import annotations

from pymongo import AsyncMongoClient

from app.core.config import settings

_client: AsyncMongoClient | None = None  # type: ignore[type-arg]


def get_db_client() -> AsyncMongoClient:  # type: ignore[type-arg]
    global _client  # noqa: PLW0603
    if _client is None:
        _client = AsyncMongoClient(str(settings.MONGODB_URL))
    return _client


def get_database() -> AsyncMongoClient:  # type: ignore[type-arg]
    return get_db_client()[settings.MONGODB_DB_NAME]


async def close_database() -> None:
    global _client  # noqa: PLW0603
    if _client is not None:
        _client.close()
        _client = None
