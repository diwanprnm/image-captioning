def test_import_app():
    """Verify app imports and has correct metadata"""
    from app.main import app

    assert app.title== "Image Captioning Service"