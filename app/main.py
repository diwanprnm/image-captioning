from fastapi import FastAPI

from app.core.config import settings
from app.api.v1 import api as api_v1_router
from app.db.session import create_db_and_tables
from contextlib import asynccontextmanager


async def lifespan(app: FastAPI):
     """FastAPI lifespan context manager for startup/shutdown events."""
    print("Application startup...")
    create_db_and_tables() # Panggil function ini saat startup
    yield # Aplikasi berjalan di sini
    print("Application shutdown.")
    # Clean up can be done here if needed

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