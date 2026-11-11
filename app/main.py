import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import setup_logging

settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # بيتنفذ مرة واحدة وقت تشغيل السيرفر
    logger.info("Application started: %s (debug=%s)", settings.app_name, settings.debug)
    yield
    # بيتنفذ مرة واحدة وقت إغلاق السيرفر
    logger.info("Application shutting down")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    logger.info("Health check called")
    return {"status": "ok"}