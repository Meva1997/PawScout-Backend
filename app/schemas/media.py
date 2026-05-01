from pydantic import BaseModel


class MediaUploadResponse(BaseModel):
    """Response model for media upload."""

    url: str
    public_id: str
    resource_type: str
    format: str
    width: int | None = None
    height: int | None = None
    bytes: int | None = None


class MediaDeleteRequest(BaseModel):
    """Request model for media deletion."""

    public_id: str
    resource_type: str = "image"
