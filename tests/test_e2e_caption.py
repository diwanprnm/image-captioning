import base64
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_e2e_caption_and_store(async_client: AsyncClient, monkeypatch):
    """End-to-end test: upload image -> get caption -> stored in DB."""

    # Mock vision service to return fixed caption
    async def mock_caption(*args, **kwargs):
        return "A black pixel"

    monkeypatch.setattr(
        "app.api.v1.endpoints.caption.get_image_caption", mock_caption
    )

    # 1x1 black pixel PNG (base64)
    png_b64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGA"
        "WjRNDwAAAABJRU5ErkJggg=="
    )
    png_bytes = base64.b64decode(png_b64)

    files = {"file": ("test.png", png_bytes, "image/png")}
    response = await async_client.post("/api/v1/caption/", files=files)

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert data["filename"] == "test.png"
    assert data["caption"] == "A black pixel"
    assert data["model_used"] == "combofreetwo"  # dari settings.NINE_ROUTER_VISION_MODEL
    assert "id" in data
    assert "created_at" in data
    assert isinstance(data["id"], int)
    assert data["id"] > 0