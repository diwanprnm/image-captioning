from fastapi import FastAPI

from app.core.config import settings
from app.api.v1 import api as api_v1_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager for startup/shutdown events."""
    create_db_and_tables() # Jalankan saat startup
    yield # Aplikasi berjalan di sini
    # Clean up can be done here if needed (e.g., close DB connections)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan # Gunakan lifespan context manager
)

app.include_router(api_v1_router.api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}