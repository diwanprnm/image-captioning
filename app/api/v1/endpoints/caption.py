from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from sqlmodel import Session

from app.core.config import settings
from app.db.session import get_session
from app.models.image_caption import ImageCaption
from app.services.vision_service import get_image_caption
from app.exceptions import VisionServiceError
from app.schemas import CaptionResponse

router = APIRouter(
    prefix="/caption",
    tags=["caption"],
    responses={404: {"description": "Not found"}},
)

MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post(
    "/",
    summary="Generate caption for an uploaded image",
    description="Upload an image (PNG, JPEG, WebP) and receive a descriptive caption. Uses a vision LLM via 9router.",
    response_description="Caption metadata including ID, filename, caption text, model used, and creation timestamp.",
    status_code=status.HTTP_200_OK,
    response_model=CaptionResponse
)
async def create_caption(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    """
    Handles image upload, calls vision service, stores result, and returns caption info.
    """
    # 1. Validasi ukuran file
    if file.size is None or file.size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large (max {MAX_UPLOAD_SIZE // 1024 // 1024}MB)",
        )

    # 2. Validasi content type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image",
        )

    # 3. Baca bytes
    image_bytes = await file.read()

    # 4. Double-check size
    if len(image_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large (max {MAX_UPLOAD_SIZE // 1024 // 1024}MB)",
        )

    # 5. Panggil vision service
    try:
        caption = await get_image_caption(image_bytes, file.content_type)
        model_name = settings.NINE_ROUTER_VISION_MODEL

    except VisionServiceError:
        raise  # Re-raise, handler akan tangkap

    except Exception as e:
        raise VisionServiceError(
            detail=f"Unexpected error calling vision service: {str(e)}"
        ) from e

    # 6. Simpan ke DB
    db_obj = ImageCaption(
        image_url=f"upload://{file.filename}",
        caption=caption,
        model_used=model_name,
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    # 7. Return response
    return {
        "id": db_obj.id,
        "filename": file.filename,
        "caption": caption,
        "model_used": db_obj.model_used,
        "created_at": db_obj.created_at.isoformat(),
    }