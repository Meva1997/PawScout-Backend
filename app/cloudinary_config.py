import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url
import os
from typing import Dict, Any
from fastapi import HTTPException, UploadFile

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    secure=True
)


async def upload_media(
    file: UploadFile,
    folder: str = "pawscout",
    resource_type: str = "auto"
) -> Dict[str, Any]:
    """
    Upload an image or video to Cloudinary.
    
    Args:
        file: UploadFile from FastAPI
        folder: Cloudinary folder to store the file
        resource_type: 'image', 'video', or 'auto'
    
    Returns:
        Dictionary with upload result including secure_url and public_id
    """
    try:
        # Read file contents
        contents = await file.read()
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type=resource_type,
            transformation=[
                {"quality": "auto", "fetch_format": "auto"}
            ] if resource_type in ["image", "auto"] else None
        )
        
        return {
            "url": upload_result["secure_url"],
            "public_id": upload_result["public_id"],
            "resource_type": upload_result["resource_type"],
            "format": upload_result["format"],
            "width": upload_result.get("width"),
            "height": upload_result.get("height"),
            "bytes": upload_result.get("bytes")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


async def delete_media(public_id: str, resource_type: str = "image") -> Dict[str, Any]:
    """
    Delete an image or video from Cloudinary.
    
    Args:
        public_id: The public_id of the file to delete
        resource_type: 'image' or 'video'
    
    Returns:
        Dictionary with deletion result
    """
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        
        if result.get("result") != "ok":
            raise HTTPException(status_code=404, detail="Media not found or already deleted")
        
        return {"message": "Media deleted successfully", "result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")


def get_optimized_url(public_id: str, width: int = 800, height: int = 600) -> str:
    """
    Generate an optimized URL for an image.
    
    Args:
        public_id: The public_id of the image
        width: Desired width
        height: Desired height
    
    Returns:
        Optimized URL string
    """
    url, _ = cloudinary_url(
        public_id,
        width=width,
        height=height,
        crop="fill",
        quality="auto",
        fetch_format="auto"
    )
    return url