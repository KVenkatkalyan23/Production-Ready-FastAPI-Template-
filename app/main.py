"""FastAPI application entry point."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.schemas.success import SuccessResponse


configure_logging(settings.LOG_LEVEL, settings.LOG_JSON)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Emit startup diagnostics for environment and config loading."""

    logger.info("Application startup")
    logger.info("Active environment: %s", settings.ENVIRONMENT)
    logger.info("Active env file: %s", settings.env_file)
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    return app


app = create_app()


@app.get("/health", response_model=SuccessResponse)
async def health_check() -> SuccessResponse:
    """Minimal health-check endpoint."""

    return SuccessResponse(
        message="Request completed successfully",
        data={"status": "healthy", "environment": settings.ENVIRONMENT},
    )
