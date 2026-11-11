import logging
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.logging import setup_logging
from pathlib import Path

from fastapi.staticfiles import StaticFiles
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from app.api.v1.router import api_router
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
app.include_router(api_router, prefix="/api/v1")
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/ui", StaticFiles(directory=STATIC_DIR, html=True), name="ui")
@app.get("/health", tags=["system"])
def health_check() -> dict:
    logger.info("Health check endpoint called")
    return {"status": "ok"}
