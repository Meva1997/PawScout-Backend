from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, select
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum
from app.database import SessionDep
from app.dependencies import AdminUser

router = APIRouter(
    prefix="/volunteer",
    tags=["volunteer"],
)

class VolunteerStatus(str, Enum):
    """Status options for volunteer applications."""
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Volunteer(SQLModel, table=True):
    """Volunteer application model for managing volunteer registrations."""
    id: int | None = Field(default=None, primary_key=True, index=True, unique=True)
    name: str = Field(min_length=1, max_length=100, description="Volunteer's first name")
    lastName: str = Field(min_length=1, max_length=100, description="Volunteer's last name")
    email: EmailStr = Field(index=True, unique=True, description="Volunteer's email address")
    phone: str = Field(min_length=7, max_length=20, description="Volunteer's phone number")
    availability: List[str] = Field(sa_column=Column(ARRAY(String)), description="Time availability (e.g., weekdays, weekends)")
    availableDays: List[str] = Field(sa_column=Column(ARRAY(String)), description="Specific days available")
    areasOfInterest: List[str] = Field(sa_column=Column(ARRAY(String)), description="Areas of interest for volunteering")
    whyVolunteer: str = Field(min_length=10, max_length=1000, description="Reason for wanting to volunteer")
    specialSkills: str = Field(min_length=1, max_length=500, description="Special skills or qualifications")
    emergencyContactName: str = Field(min_length=1, max_length=100, description="Emergency contact name")
    emergencyContactPhone: str = Field(min_length=7, max_length=20, description="Emergency contact phone number")
    status: VolunteerStatus = Field(default=VolunteerStatus.pending, description="Application status")
    privacyAgreement: bool = Field(default=False, description="Agreement to privacy policy")
    date: str = Field(description="Application submission date")

 
def existing_volunteer_email(session: SessionDep, email: str) -> bool:
    volunteer = session.exec(select(Volunteer).where(Volunteer.email == email)).first()
    return volunteer is not None

def existing_voluneer_phone(session: SessionDep, phone: str) -> bool:
    volunteer = session.exec(select(Volunteer).where(Volunteer.phone == phone)).first()
    return volunteer is not None

def volunteer_not_found(session: SessionDep, volunteer_id: int) -> None:
    volunteer = session.get(Volunteer, volunteer_id)
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
 


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Submit volunteer application",
    description="Submit a new volunteer application. Email and phone must be unique. Privacy agreement must be accepted.",
    responses={
        201: {"description": "Volunteer application submitted successfully"},
        400: {"description": "Invalid input - empty fields, missing privacy agreement, or validation errors"},
        409: {"description": "Email or phone number already registered"}
    }
)
async def create_volunteer(volunteer: Volunteer, session: SessionDep):

    if existing_volunteer_email(session, volunteer.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    if existing_voluneer_phone(session, volunteer.phone):
        raise HTTPException(status_code=409, detail="Phone number already registered")

    for field, value in volunteer.dict().items():
        if field == "id" or field == "status":
            continue

        if isinstance(value, str) and value.strip() == "":
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

        if isinstance(value, list) and len(value) == 0:
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")
        
        if field == "privacyAgreement" and value is not True:
                raise HTTPException(status_code=400, detail="You must agree to the privacy policy")

    session.add(volunteer)
    session.commit()
    session.refresh(volunteer)
    return {"success": "Volunteer form successfully submitted"}

@router.get(
    "/{volunteer_id}",
    status_code=status.HTTP_200_OK,
    summary="Get volunteer by ID",
    description="Retrieve details of a specific volunteer application. Requires admin privileges.",
    responses={
        200: {"description": "Volunteer found"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"},
        404: {"description": "Volunteer not found"}
    }
)
async def read_volunteer(volunteer_id: int, session: SessionDep, admin: AdminUser):
    volunteer = session.get(Volunteer, volunteer_id)
    volunteer_not_found(session, volunteer_id)
    return volunteer

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all volunteers",
    description="Retrieve a list of all volunteer applications with their current status. Requires admin privileges.",
    responses={
        200: {"description": "List of all volunteers"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"}
    }
)
async def read_volunteers(session: SessionDep, admin: AdminUser):
    volunteers = session.exec(select(Volunteer)).all()
    return {"volunteers": volunteers}

@router.put(
    "/{volunteer_id}",
    status_code=status.HTTP_200_OK,
    summary="Update volunteer application",
    description="Update an existing volunteer's information. Email and phone uniqueness will be validated if changed. Requires admin privileges.",
    responses={
        200: {"description": "Volunteer updated successfully or no changes detected"},
        400: {"description": "Invalid input - empty fields or validation errors"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"},
        404: {"description": "Volunteer not found"},
        409: {"description": "Email or phone number already registered to another volunteer"}
    }
)
async def update_volunteer(volunteer_id: int, updated_volunteer: Volunteer, session: SessionDep, admin: AdminUser):
    volunteer = session.get(Volunteer, volunteer_id)
    volunteer_not_found(session, volunteer_id)

    if volunteer.email != updated_volunteer.email:
        if existing_volunteer_email(session, updated_volunteer.email):
            raise HTTPException(status_code=409, detail="Email already registered")
    
    if volunteer.phone != updated_volunteer.phone:
        if existing_voluneer_phone(session, updated_volunteer.phone):
            raise HTTPException(status_code=409, detail="Phone number already registered")

    changes_made = False
    for field, value in updated_volunteer.dict().items():
        if field == "id":
            continue

        if isinstance(value, str) and value.strip() == "":
            raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

        if isinstance(value, list) and len(value) == 0:
            raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

        if getattr(volunteer, field) != value:
            setattr(volunteer, field, value) # setattr to update fields
            changes_made = True
        
    if not changes_made:
        return {"message": "No changes detected"}

    session.add(volunteer)
    session.commit()
    session.refresh(volunteer)

    return {"success": "Volunteer updated successfully"}

@router.delete(
    "/{volunteer_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete volunteer application",
    description="Permanently delete a volunteer application from the system. This action cannot be undone. Requires admin privileges.",
    responses={
        200: {"description": "Volunteer deleted successfully"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"},
        404: {"description": "Volunteer not found"}
    }
)
async def delete_volunteer(volunteer_id: int, session: SessionDep, admin: AdminUser):
    volunteer = session.get(Volunteer, volunteer_id)

    volunteer_not_found(session, volunteer_id)

    session.delete(volunteer)
    session.commit()

    return {"success": "Volunteer form deleted successfully"}