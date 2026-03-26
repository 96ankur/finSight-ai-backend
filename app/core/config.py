from __future__ import annotations

from typing import Any

from pydantic import Field, MongoDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "FastAPI Boilerplate"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # MongoDB
    MONGODB_URL: MongoDsn = MongoDsn("mongodb://localhost:27017")  # type: ignore[arg-type]
    MONGODB_DB_NAME: str = "fastapi_boilerplate"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Logging
    LOG_LEVEL: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @model_validator(mode="before")
    @classmethod
    def validate_production_settings(cls, values: dict[str, Any]) -> dict[str, Any]:
        if values.get("APP_ENV") == "production" and values.get("DEBUG"):
            msg = "DEBUG must be False in production"
            raise ValueError(msg)
        return values


settings = Settings()  # type: ignore[call-arg]
