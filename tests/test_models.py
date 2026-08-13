from datetime import datetime


def test_image_caption_model_fields():
    """Verify ImageCaption model can be instantiated with correct fields."""
    from app.models.image_caption import ImageCaption

    ic = ImageCaption(
        image_url="http://example.com/img.jpg",
        caption="A test caption",
        model_used="gemini-pro-vision",
        created_at=datetime(2023, 1, 1, 12, 0, 0) # Fixed datetime for testing
    )

    assert ic.image_url == "http://example.com/img.jpg"
    assert ic.caption == "A test caption"
    assert ic.model_used == "gemini-pro-vision"
    assert ic.id is None  # Not yet persisted to DB
    assert ic.created_at == datetime(2023, 1, 1, 12, 0, 0)