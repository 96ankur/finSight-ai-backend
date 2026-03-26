from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import get_logger, setup_logging
from app.db.init_db import init_db, close_db

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown events."""
    setup_logging()
    logger.info("application_starting")

    # await init_db()
    logger.info("database_connected")

    yield

    await close_db()
    logger.info("application_shutdown")
