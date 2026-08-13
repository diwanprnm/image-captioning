from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ImageCaption(SQLModel, table=True):
    """
    Represents an image caption entry in database.
    `table=True` makes it a SQLModel model that corresponds to a database table.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    image_url: str = Field(index=True)
    caption: str
    model_used: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # pydantic_settings/SQLModel V2 compatibility
    # https://sqlmodel.tiangolo.com/tutorial/where/#protected-namespaces-on-pydantic-v2
    # This setting is necessary to avoid warnings with Pydantic V2 and SQLModel.

    model_config = {"protected_namespaces": ()}