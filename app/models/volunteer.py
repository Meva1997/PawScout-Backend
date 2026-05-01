from enum import Enum
from typing import List

from pydantic import EmailStr
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, SQLModel


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
    availability: List[str] = Field(
        sa_column=Column(ARRAY(String)),
        description="Time availability (e.g., weekdays, weekends)",
    )
    availableDays: List[str] = Field(
        sa_column=Column(ARRAY(String)),
        description="Specific days available",
    )
    areasOfInterest: List[str] = Field(
        sa_column=Column(ARRAY(String)),
        description="Areas of interest for volunteering",
    )
    whyVolunteer: str = Field(min_length=10, max_length=1000, description="Reason for wanting to volunteer")
    specialSkills: str = Field(min_length=1, max_length=500, description="Special skills or qualifications")
    emergencyContactName: str = Field(min_length=1, max_length=100, description="Emergency contact name")
    emergencyContactPhone: str = Field(min_length=7, max_length=20, description="Emergency contact phone number")
    status: VolunteerStatus = Field(default=VolunteerStatus.pending, description="Application status")
    privacyAgreement: bool = Field(default=False, description="Agreement to privacy policy")
    date: str = Field(description="Application submission date")
