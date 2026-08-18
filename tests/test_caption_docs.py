import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_caption_endpoint_in_openapi_schema(async_client: AsyncClient):
    """Verify /caption endpoint appears in OpenAPI schema with correct summary."""
    response = await async_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()

    path = schema["paths"].get("/api/v1/caption/")
    assert path is not None
    assert path["post"]["summary"] == "Generate caption for an uploaded image"

    # Check response schema references CaptionResponse
    response_schema = path["post"]["responses"]["200"]
    assert "application/json" in response_schema["content"]