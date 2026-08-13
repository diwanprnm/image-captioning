from fastapi import HTTPException


class VisionServiceError(HTTPException):
    """Raised when vision LLM call fails."""
    def __init__(self, detail: str = "Vision service unavailable"):
        super().__init__(status_code=502, detail=detail)