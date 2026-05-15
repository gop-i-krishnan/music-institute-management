from pydantic import BaseModel
from typing import Optional, Any


# Shared response wrapper used by routes that return a message, data, and metadata.
class StandardResponse(BaseModel):
    # Indicates whether the request completed successfully.
    success: bool

    # Human-readable message describing the result.
    message: str

    # Optional payload for the response, such as a record or list of records.
    data: Optional[Any] = None

    # Optional extra information, such as pagination totals and current page.
    meta: Optional[dict] = None

    # Allows Pydantic to read values directly from ORM/model objects.
    model_config = {"from_attributes": True}
