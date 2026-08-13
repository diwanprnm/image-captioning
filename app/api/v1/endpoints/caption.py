from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from sqlmodel import Session
from app.core.config import settings
from app.db.session import get_session
from app.models.image_caption import ImageCaption
from app.services.vision_service import get_image_caption
from app.exceptions import VisionServiceError

router = APIRouter(
    prefix="/caption",
    tags =["caption"],
    responses= {404:{"description": "Not Found"}},
)

MAX_UPLOAD_SIZE = 5 * 1024 * 1024 #5MB

@router.post(
    "/",
    summary= "Generate caption for an uploaded image",
    description= "Upload an image (PNG, JPEG, WebP) and receive a descriptive caption. Uses a vision LLM via 9router.",
    response_description= "Caption metadata including ID, filename, caption text, model used, and creation timestamp.",
    status_code= status.HTTP_200_OK,
    response_model= dict,
)
async def create_caption(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
):
    """
    Handles image upload, calls vision service, stores result, and returns caption info.
    """
    if file.size is None or file.size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code = status.HTTP_413_REQUEST_ENTIRY_TOO_LARGE,
            detail = f"File too large (max {MAX_UPLOAD_SIZE // 1024 // 1024}MB)",
        )

        if not file.content_type.startswith("/image"):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "File must be an image"
            )
    image_bytes = await file.read()

    try:
        caption = await get_image_caption(image_bytes, file.content_type)
        model_name = settings.NINE_ROUTER_VISION_MODEL
    except VisionServiceError as e:
        raise VisionServiceError(detail=f"Unexpected error calling vision service: {str(e)}") from e
    
     # Save to DB (Optional, depends on Task 5)
    # db_obj = ImageCaption(
    #     image_url=f"upload://{file.filename}",
    #     caption=caption,
    #     model_used=model_name
    # )
    # session.add(db_obj)
    # session.commit()
    # session.refresh(db_obj)

    return {
        "filename": file.filename,
        "caption": caption or "Placeholder caption - Vision service not yet implemented.", # Use placeholder if vision not ready
        "model_used": model_name,
        # "id": db_obj.id,
        # "created_at": db_obj.created_at.isoformat(),
    }

