from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}