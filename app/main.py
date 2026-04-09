"""FastAPI application entry point."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.schemas.success import SuccessResponse


configure_logging(settings.LOG_LEVEL, settings.LOG_JSON)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def log_startup() -> None:
    """Emit startup diagnostics for environment and config loading."""

    logger.info("Application startup")
    logger.info("Active environment: %s", settings.ENVIRONMENT)
    logger.info("Active env file: %s", settings.env_file)


@app.get("/health", response_model=SuccessResponse)
async def health_check() -> SuccessResponse:
    """Minimal health-check endpoint."""

    return SuccessResponse(
        message="Request completed successfully",
        data={"status": "healthy", "environment": settings.ENVIRONMENT},
    )
