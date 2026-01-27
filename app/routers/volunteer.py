from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, Field, select
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum
from app.database import SessionDep

router = APIRouter()

class VolunteerStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Volunteer(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True, unique=True)
    name: str
    lastName: str
    email: str = Field(index=True, unique=True)
    phone: str
    availability: List[str] = Field(sa_column=Column(ARRAY(String)))
    availableDays: List[str] = Field(sa_column=Column(ARRAY(String)))
    areasOfInterest: List[str] = Field(sa_column=Column(ARRAY(String)))
    whyVolunteer: str
    specialSkills: str
    emergencyContactName: str
    emergencyContactPhone: str
    status: VolunteerStatus = Field(default=VolunteerStatus.pending)
    privacyAgreement: bool = Field(default=False)

 
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



@router.post("/volunteers")
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

@router.get("/volunteers/{volunteer_id}")
async def read_volunteer(volunteer_id: int, session: SessionDep):
    volunteer = session.get(Volunteer, volunteer_id)
    volunteer_not_found(session, volunteer_id)
    return volunteer

@router.get("/volunteers")
async def read_volunteers(session: SessionDep):
    volunteers = session.exec(select(Volunteer)).all()
    return {"volunteers": volunteers}

@router.put("/volunteers/{volunteer_id}")
async def update_volunteer(volunteer_id: int, updated_volunteer: Volunteer, session: SessionDep):
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