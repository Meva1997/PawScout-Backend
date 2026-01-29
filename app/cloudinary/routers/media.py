from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, status
from pydantic import BaseModel
from app.cloudinary_config import upload_media, delete_media
from app.dependencies import AdminUser

router = APIRouter(
    prefix="/media",
    tags=["media"],
)


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
    resource_type: str = "image"  # 'image' or 'video'


@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=MediaUploadResponse,
    summary="Upload image or video to Cloudinary",
    description="Upload a single image or video file. Supports jpg, png, gif, mp4, mov, etc. Admin only.",
    responses={
        201: {"description": "Media uploaded successfully"},
        400: {"description": "Invalid file format"},
        401: {"description": "Not authenticated"},
        403: {"description": "Admin privileges required"},
        500: {"description": "Upload failed"}
    }
)
async def upload_media_file(
    admin: AdminUser,
    file: UploadFile = File(..., description="Image or video file to upload")
):
    """
    Upload an image or video to Cloudinary.
    Automatically detects file type and optimizes accordingly.
    """
    # Validate file type
    allowed_types = [
        "image/jpeg", "image/png", "image/gif", "image/webp",
        "video/mp4", "video/quicktime", "video/x-msvideo"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: images (jpg, png, gif, webp) and videos (mp4, mov, avi)"
        )
    
    # Determine resource type
    resource_type = "video" if file.content_type.startswith("video/") else "image"
    
    # Upload to Cloudinary
    result = await upload_media(file, folder="pawscout/animals", resource_type=resource_type)
    
    return MediaUploadResponse(**result)


@router.post(
    "/upload-multiple",
    status_code=status.HTTP_201_CREATED,
    response_model=List[MediaUploadResponse],
    summary="Upload multiple images/videos",
    description="Upload multiple media files at once. Admin only.",
    responses={
        201: {"description": "All media uploaded successfully"},
        400: {"description": "Invalid file format in one or more files"},
        401: {"description": "Not authenticated"},
        403: {"description": "Admin privileges required"},
        500: {"description": "Upload failed"}
    }
)
async def upload_multiple_media(
    admin: AdminUser,
    files: List[UploadFile] = File(..., description="Multiple image or video files")
):
    """
    Upload multiple images or videos to Cloudinary.
    Useful for adding multiple photos to an animal profile.
    """
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files per upload")
    
    results = []
    
    for file in files:
        # Validate file type
        allowed_types = [
            "image/jpeg", "image/png", "image/gif", "image/webp",
            "video/mp4", "video/quicktime", "video/x-msvideo"
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type in '{file.filename}'. Allowed: images and videos"
            )
        
        # Determine resource type
        resource_type = "video" if file.content_type.startswith("video/") else "image"
        
        # Upload to Cloudinary
        result = await upload_media(file, folder="pawscout/animals", resource_type=resource_type)
        results.append(MediaUploadResponse(**result))
    
    return results


@router.delete(
    "/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete media from Cloudinary",
    description="Delete an image or video from Cloudinary by public_id. Admin only.",
    responses={
        200: {"description": "Media deleted successfully"},
        401: {"description": "Not authenticated"},
        403: {"description": "Admin privileges required"},
        404: {"description": "Media not found"},
        500: {"description": "Delete failed"}
    }
)
async def delete_media_file(admin: AdminUser, media: MediaDeleteRequest):
    """
    Delete an image or video from Cloudinary.
    Requires the public_id returned when the file was uploaded.
    """
    result = await delete_media(media.public_id, media.resource_type)
    return result
