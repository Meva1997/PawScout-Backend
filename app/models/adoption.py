from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class AdoptionStatus(str, Enum):
    """Status options for adoption applications."""

    approved = "approved"
    pending = "pending"
    rejected = "rejected"


class AdoptionApplication(SQLModel, table=True):
    """Adoption application model for processing animal adoption requests."""

    id: int | None = Field(default=None, primary_key=True, index=True)
    animalId: int = Field(foreign_key="animal.id", index=True, description="ID of the animal being adopted")
    applicantName: str = Field(min_length=1, max_length=100, description="Applicant's first name")
    applicantLastName: str = Field(min_length=1, max_length=100, description="Applicant's last name")
    email: EmailStr = Field(description="Applicant's email address")
    phone: str = Field(min_length=7, max_length=20, description="Applicant's phone number")
    address: str = Field(min_length=5, max_length=200, description="Street address")
    city: str = Field(min_length=2, max_length=100, description="City")
    state: str = Field(min_length=2, max_length=100, description="State or province")
    zipCode: str = Field(min_length=3, max_length=20, description="Postal/ZIP code")
    birthdate: str = Field(description="Applicant's birthdate")
    occupation: str = Field(min_length=2, max_length=100, description="Applicant's occupation")
    reasonForAdoption: str = Field(min_length=10, max_length=1000, description="Reason for wanting to adopt")
    experienceWithPets: str = Field(min_length=5, max_length=1000, description="Previous experience with pets")
    homeType: str = Field(min_length=2, max_length=50, description="Type of home (apartment, house, etc.)")
    whoLivesInHouse: str = Field(min_length=1, max_length=500, description="Who lives in the household")
    agreeToTerms: bool = Field(description="Agreement to terms and conditions")
    date: str = Field(description="Application submission date")
    status: AdoptionStatus = Field(
        default=AdoptionStatus.pending,
        description="Application status (pending, approved, rejected)",
    )
