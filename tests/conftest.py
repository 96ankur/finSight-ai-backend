from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Provide an async test client with a test database.

    Uses dependency overrides and mongomock to avoid requiring a real MongoDB instance.
    """
    from mongomock_motor import AsyncMongoMockClient
    from beanie import init_beanie

    from app.db.init_db import DOCUMENT_MODELS
    from app.main import app

    mock_client = AsyncMongoMockClient()
    db = mock_client["test_db"]
    await init_beanie(database=db, document_models=DOCUMENT_MODELS)  # type: ignore[arg-type]

    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
