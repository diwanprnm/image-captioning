from datetime import datetime
from pydantic import BaseModel

class CaptionResponse(BaseModel):
    """Schema for /caption endpoint response"""
    id : int
    filename: str
    caption: str
    model_used: str
    created_at: datetime
