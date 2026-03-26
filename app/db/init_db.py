from __future__ import annotations

from beanie import init_beanie

from app.db.mongo import close_database, get_database

DOCUMENT_MODELS = []


async def init_db() -> None:
    """Initialize Beanie with document models."""
    database = get_database()
    await init_beanie(database=database, document_models=DOCUMENT_MODELS)  # type: ignore[arg-type]


async def close_db() -> None:
    """Close the database connection."""
    await close_database()
