from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.events import lifespan
from app.exceptions.base import AppException
from app.middleware.correlation_id import CorrelationIdMiddleware
from app.middleware.logging import RequestLoggingMiddleware


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    _setup_middleware(application)
    _setup_exception_handlers(application)
    _setup_routes(application)

    return application


def _setup_middleware(application: FastAPI) -> None:
    application.add_middleware(CorrelationIdMiddleware)
    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if settings.is_production:
        application.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])


def _setup_exception_handlers(application: FastAPI) -> None:
    @application.exception_handler(AppException)
    async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )


def _setup_routes(application: FastAPI) -> None:
    application.include_router(api_router)


app = create_app()
