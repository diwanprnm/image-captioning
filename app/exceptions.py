from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class VisionServiceError(HTTPException):
    """Raised when vision LLM call fails.   """
    def __init__(self, detail: str = "Vision service unavailable"):
        super().__init__(status_code=502, detail=detail)

async def vision_service_exception_handler(request: Request, exc: VisionServiceError):
    """Convert VisionServiceError to JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )