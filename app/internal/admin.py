from fastapi import APIRouter, HTTPException, UploadFile, File, status
from sqlmodel import select
from datetime import datetime
from app.dependencies import AdminUser, SessionDep
from app.routers.users import PawUser
from app.routers.animals import Animal
from app.routers.adopt import AdoptionApplication
from app.routers.volunteer import Volunteer
from app.cloudinary_config import upload_media, delete_media
from app.models.settings import ShelterSettings, ShelterSettingsUpdate

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={
        401: {"description": "Not authenticated - invalid or missing token"},
        403: {"description": "Forbidden - admin privileges required"}
    }
)


@router.get(
    "/dashboard",
    status_code=status.HTTP_200_OK,
    summary="Get admin dashboard statistics",
    description="Retrieve overview statistics for the admin dashboard including total counts of users, animals, adoptions, and volunteers. Requires admin authentication.",
    responses={
        200: {"description": "Dashboard statistics retrieved successfully"}
    }
)
async def get_admin_dashboard(admin: AdminUser, session: SessionDep):
    """Admin dashboard with statistics overview."""
    # Get counts
    total_users = len(session.exec(select(PawUser)).all())
    total_animals = len(session.exec(select(Animal)).all())
    total_adoptions = len(session.exec(select(AdoptionApplication)).all())
    total_volunteers = len(session.exec(select(Volunteer)).all())
    
    return {
        "message": f"Welcome to admin dashboard, {admin.name}!",
        "stats": {
            "total_users": total_users,
            "total_animals": total_animals,
            "total_adoptions": total_adoptions,
            "total_volunteers": total_volunteers
        }
    }


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    summary="Get all registered users",
    description="Retrieve a list of all registered users in the system. Passwords are excluded from the response for security. Admin only.",
    responses={
        200: {"description": "List of all users (without passwords)"}
    }
)
async def get_all_users(admin: AdminUser, session: SessionDep):
    """Get all registered users. Admin only endpoint."""
    users = session.exec(select(PawUser)).all()
    # Don't return passwords
    return [
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "lastName": user.lastName,
            "isAdmin": user.isAdmin
        }
        for user in users
    ]


@router.patch(
    "/users/{user_id}/promote",
    status_code=status.HTTP_200_OK,
    summary="Promote user to admin",
    description="Grant admin privileges to a regular user. The user must exist and not already be an admin. Admin only.",
    responses={
        200: {"description": "User promoted to admin successfully"},
        400: {"description": "User is already an admin"},
        404: {"description": "User not found"}
    }
)
async def promote_user_to_admin(user_id: int, admin: AdminUser, session: SessionDep):
    """Promote a user to admin status. Admin only endpoint."""
    user = session.get(PawUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.isAdmin:
        raise HTTPException(status_code=400, detail="User is already an admin")
    
    user.isAdmin = True
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {
        "message": f"User {user.email} promoted to admin successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "isAdmin": user.isAdmin
        }
    }


@router.patch(
    "/users/{user_id}/demote",
    status_code=status.HTTP_200_OK,
    summary="Remove admin privileges from user",
    description="Revoke admin privileges from a user. Cannot demote yourself. The user must exist and be an admin. Admin only.",
    responses={
        200: {"description": "Admin privileges removed successfully"},
        400: {"description": "User is not an admin or attempting to demote yourself"},
        404: {"description": "User not found"}
    }
)
async def demote_admin_to_user(user_id: int, admin: AdminUser, session: SessionDep):
    """Remove admin privileges from a user. Admin only endpoint."""
    user = session.get(PawUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.isAdmin:
        raise HTTPException(status_code=400, detail="User is not an admin")
    
    # Prevent demoting yourself
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot demote yourself")
    
    user.isAdmin = False
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {
        "message": f"Admin privileges removed from {user.email}",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "isAdmin": user.isAdmin
        }
    }


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user from system",
    description="Permanently remove a user from the system. Cannot delete yourself. This action cannot be undone. Admin only.",
    responses={
        200: {"description": "User deleted successfully"},
        400: {"description": "Attempting to delete yourself"},
        404: {"description": "User not found"}
    }
)
async def delete_user(user_id: int, admin: AdminUser, session: SessionDep):
    """Delete a user from the system. Admin only endpoint."""
    user = session.get(PawUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deleting yourself
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    session.delete(user)
    session.commit()
    
    return {"message": f"User {user.email} deleted successfully"}


@router.get(
    "/adoptions",
    status_code=status.HTTP_200_OK,
    summary="Get all adoption applications",
    description="Retrieve all adoption applications with complete details for admin review. Admin only.",
    responses={
        200: {"description": "List of all adoption applications"}
    }
)
async def get_all_adoptions(admin: AdminUser, session: SessionDep):
    """Get all adoption applications with full details. Admin only endpoint."""
    adoptions = session.exec(select(AdoptionApplication)).all()
    return {"requests": adoptions}


@router.get(
    "/volunteers",
    status_code=status.HTTP_200_OK,
    summary="Get all volunteer applications",
    description="Retrieve all volunteer applications for admin review and management. Admin only.",
    responses={
        200: {"description": "List of all volunteer applications"}
    }
)
async def get_all_volunteers(admin: AdminUser, session: SessionDep):
    """Get all volunteer applications. Admin only endpoint."""
    volunteers = session.exec(select(Volunteer)).all()
    return volunteers

@router.post(
    "/logo",
    status_code=status.HTTP_200_OK,
    summary="Post shelter logo",
    description="Upload shelter logo image to Cloudinary and save to database. Admin only.",
    responses={
        200: {"description": "Shelter logo uploaded successfully"},
        400: {"description": "Invalid file format"},
        500: {"description": "Upload failed"}
    }
)
async def post_shelter_logo(
    admin: AdminUser,
    session: SessionDep,
    file: UploadFile = File(..., description="Logo image file to upload")
):
    """Upload the shelter's logo to Cloudinary and save to database. Admin only endpoint."""
    # Validate file type - only accept images
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Allowed: jpg, png, gif, webp"
        )
    
    # Get existing settings (should be only one record)
    statement = select(ShelterSettings)
    existing_settings = session.exec(statement).first()
    
    # If there's an old logo, delete it from Cloudinary
    if existing_settings and existing_settings.logo_public_id:
        try:
            await delete_media(existing_settings.logo_public_id, "image")
        except Exception:
            # Continue even if deletion fails
            pass
    
    # Upload new logo to Cloudinary
    result = await upload_media(file, folder="pawscout/settings", resource_type="image")
    
    # Update or create settings record
    if existing_settings:
        existing_settings.logo_url = result["url"]
        existing_settings.logo_public_id = result["public_id"]
        existing_settings.updated_at = datetime.utcnow()
        session.add(existing_settings)
    else:
        new_settings = ShelterSettings(
            logo_url=result["url"],
            logo_public_id=result["public_id"]
        )
        session.add(new_settings)
    
    session.commit()
    session.refresh(existing_settings if existing_settings else new_settings)
    
    return {
        "message": "Shelter logo uploaded and saved successfully",
        "logo_url": result["url"],
        "public_id": result["public_id"]
    }

@router.get(
    "/logo",
    status_code=status.HTTP_200_OK,
    summary="Get shelter logo",
    description="Retrieve the current shelter logo URL. Public endpoint.",
    responses={
        200: {"description": "Shelter logo retrieved successfully"},
        404: {"description": "Logo not found"}
    }
)
async def get_shelter_logo(session: SessionDep):
    """Get the current shelter logo URL. Public endpoint."""
    statement = select(ShelterSettings)
    settings = session.exec(statement).first()
    
    if not settings or not settings.logo_url:
        raise HTTPException(status_code=404, detail="Shelter logo not found")
    
    return {"logo_url": settings.logo_url}

@router.get(
    "/settings",
    status_code=status.HTTP_200_OK,
    summary="Get shelter settings",
    description="Retrieve current shelter settings including logo. Public endpoint.",
    responses={
        200: {"description": "Shelter settings retrieved successfully"},
        404: {"description": "Settings not found"}
    }
)
async def get_shelter_settings(session: SessionDep):
    """Get current shelter settings. Public endpoint."""
    statement = select(ShelterSettings)
    settings = session.exec(statement).first()
    
    if not settings:
        # Return default settings if none exist
        return {
            "logo_url": None,
            "shelter_name": "PawScout Shelter",
            "shelter_email": None,
            "shelter_phone": None,
            "shelter_address": None,
            "city": None,
            "state": None,
            "zip_code": None
        }
    
    return settings


@router.put(
    "/settings",
    status_code=status.HTTP_200_OK,
    summary="Update shelter settings",
    description="Update shelter information including name, contact details, and address. Admin only.",
    responses={
        200: {"description": "Shelter settings updated successfully"},
        400: {"description": "Invalid data provided"},
        404: {"description": "Settings not found"}
    }
)
async def update_shelter_settings(
    admin: AdminUser,
    session: SessionDep,
    settings_update: ShelterSettingsUpdate
):
    """Update shelter settings. Admin only endpoint."""
    # Get existing settings
    statement = select(ShelterSettings)
    existing_settings = session.exec(statement).first()
    
    # If no settings exist, create new record
    if not existing_settings:
        new_settings = ShelterSettings(
            shelter_name=settings_update.shelter_name or "PawScout Shelter",
            shelter_email=settings_update.shelter_email,
            shelter_phone=settings_update.shelter_phone,
            shelter_address=settings_update.shelter_address,
            city=settings_update.city,
            state=settings_update.state,
            zip_code=settings_update.zip_code,
            updated_at=datetime.utcnow()
        )
        session.add(new_settings)
        session.commit()
        session.refresh(new_settings)
        return {
            "message": "La configuración del refugio se ha creado exitosamente",
            "settings": new_settings
        }
    
    # Update only provided fields
    update_data = settings_update.model_dump(exclude_unset=True)
    
    # Check if any field has actually changed
    has_changes = False
    for field, value in update_data.items():
        current_value = getattr(existing_settings, field)
        if current_value != value:
            has_changes = True
            break
    
    # If no changes detected, return early
    if not has_changes:
        return {
            "message": "No se detectaron cambios. Los datos son idénticos a los actuales.",
            "settings": existing_settings
        }
    
    # Apply updates
    for field, value in update_data.items():
        setattr(existing_settings, field, value)
    
    existing_settings.updated_at = datetime.utcnow()
    
    session.add(existing_settings)
    session.commit()
    session.refresh(existing_settings)
    
    return {
        "message": "La configuración del refugio se ha actualizado exitosamente",
        "settings": existing_settings
    }