import logging
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.logging import setup_logging

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

settings=get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting up...")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan
)
@app.get("/health", tags=["system"])
def health_check() -> dict:
    logger.info("Health check endpoint called")
    return {"status": "ok"}
