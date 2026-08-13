import base64
import httpx

from app.core.config import settings

async def get_image_caption(image_bytes: bytes, mime_type: str) -> str:
    """
    Call vision-enabled LLM via 9router (OpenAI-compatible endpoint).
    Returns descriptive caption suitable for alt-text.

    Uses chat/completions with image_url content (data URI).
    """

    b64_image = base64.b64encode(image_bytes).decode('utf-8')

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image in one sentence suitable for alt-text.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{b64_image}"},
                },
            ],
        }
    ]

    payload = {
        "model": settings.NINE_ROUTER_VISION_MODEL,
        "messages": messages,
        "max_tokens": 200,
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {settings.NINE_ROUTER_API_KEY}",
        "Content_type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(   # ← WAJIB await
            f"{settings.NINE_ROUTER_BASE_URL.rstrip('/')}/chat/completions",
            json=payload,
            headers=headers,
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()

    content = data["choices"][0]["message"]["content"].strip()
    return content