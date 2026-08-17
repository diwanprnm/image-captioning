import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_caption_rejects_large_file(async_client: AsyncClient):
    """File > 5MB should be rejected with 413."""
    large_data = b"x" * 6 * 1024 * 1024  # 6 MB
    files = {"file": ("big.png", large_data, "image/png")}
    response = await async_client.post("/api/v1/caption/", files=files)
    assert response.status_code == 413
    assert "too large" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_caption_rejects_non_image(async_client: AsyncClient):
    """Non-image content type should be rejected with 400."""
    files = {"file": ("test.txt", b"not an image", "text/plain")}
    response = await async_client.post("/api/v1/caption/", files=files)
    assert response.status_code == 400
    assert "must be an image" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_caption_handles_vision_error(async_client: AsyncClient, monkeypatch):
    """Vision service error should return 502."""
    from app.services.vision_service import get_image_caption

    async def failing_get_caption(*args, **kwargs):
        raise RuntimeError("Vision API down")

    monkeypatch.setattr("app.api.v1.endpoints.caption.get_image_caption", failing_get_caption)

    files = {"file": ("test.png", b"fake-image-data", "image/png")}
    response = await async_client.post("/api/v1/caption/", files=files)
    assert response.status_code == 502
    assert "vision service" in response.json()["detail"].lower()