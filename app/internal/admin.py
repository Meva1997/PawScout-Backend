from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.dependencies import AdminUser, SessionDep
from app.routers.users import PawUser
from app.routers.animals import Animal
from app.routers.adopt import AdoptionApplication
from app.routers.volunteer import Volunteer

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
    return adoptions


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
