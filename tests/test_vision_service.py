import base64

import pytest


@pytest.mark.asyncio
async def test_vision_service_calls_router(monkeypatch):
    """Verify vision_service hits /chat/completions and parses response."""
    from app.services.vision_service import get_image_caption

    class MockResponse:
        status_code = 200

        def json(self):
            return {
                "choices": [
                    {"message": {"content": "A beautiful sunset over the ocean."}}
                ]
            }

        def raise_for_status(self):
            pass

    captured = {}

    class MockAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, url, json=None, headers=None, timeout=None):
            captured["url"] = url
            captured["json"] = json
            captured["headers"] = headers
            return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient", lambda: MockAsyncClient())

    # Force settings values (Settings cached on import)
    from app.core.config import settings

    settings.NINE_ROUTER_BASE_URL = "http://testrouter"
    settings.NINE_ROUTER_API_KEY="***"
    settings.NINE_ROUTER_VISION_MODEL = "gpt-4-vision-preview"

    result = await get_image_caption(b"fake-image-bytes", "image/png")

    assert result == "A beautiful sunset over the ocean."
    assert "/chat/completions" in captured["url"]
    assert captured["headers"]["Authorization"] == "Bearer ***"
    # Check image was base64-encoded in payload
    msg = captured["json"]["messages"][0]["content"]
    assert msg[0]["type"] == "text"
    assert msg[1]["type"] == "image_url"
    assert "data:image/png;base64," in msg[1]["image_url"]["url"]
    # Verify base64 of b"fake-image-bytes"
    expected_b64 = base64.b64encode(b"fake-image-bytes").decode("utf-8")
    assert msg[1]["image_url"]["url"] == f"data:image/png;base64,{expected_b64}"