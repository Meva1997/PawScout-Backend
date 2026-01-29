from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, select
from app.database import SessionDep
from app.routers.animals import Animal



router = APIRouter(
    prefix="/adopt",
    tags=["adopt"],
)


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
    reasonForAdoption: str = Field(min_length=10, max_length=1000, description="Reason for wanting to adopt")
    experienceWithPets: str = Field(min_length=5, max_length=1000, description="Previous experience with pets")
    homeType: str = Field(min_length=2, max_length=50, description="Type of home (apartment, house, etc.)")
    whoLivesInHouse: str = Field(min_length=1, max_length=500, description="Who lives in the household")
    agreeToTerms: bool = Field(description="Agreement to terms and conditions")
    date: str = Field(description="Application submission date")


@router.post(
    "/{animal_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Submit adoption application",
    description="Submit an adoption application for a specific animal. The animal's status will be updated to 'pending'. All fields must be provided and validated.",
    responses={
        201: {"description": "Adoption application submitted successfully"},
        400: {"description": "Invalid input - empty fields or validation errors"},
        404: {"description": "Animal not found"},
        409: {"description": "Animal already in adoption process (pending or adopted)"}
    }
)
async def submit_adoption_application(
    animal_id: int, application: AdoptionApplication, session: SessionDep
):

    #verify if animal exists with the given animal_id
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    if animal.availableForAdoption in ["pending", "adopted"]:
        raise HTTPException(status_code=409, detail="Animal is already in adoption process")

    for field, value in application.dict().items():
        if field in ["id", "animalId"]:
            continue

        if isinstance(value, str) and value.strip() == "":
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

    # Set animal status to pending
    animal.availableForAdoption = "pending"
    session.add(animal)

    session.add(application)
    session.commit()
    session.refresh(application)
    return {"success": "Adoption application submitted successfully"}


@router.get(
    "/{application_id}",
    status_code=status.HTTP_200_OK,
    summary="Get adoption application by ID",
    description="Retrieve details of a specific adoption application.",
    responses={
        200: {"description": "Application found"},
        404: {"description": "Application not found"}
    }
)
async def get_adoption_application(application_id: int, session: SessionDep):
    application = session.get(AdoptionApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all adoption applications",
    description="Retrieve a list of all adoption applications submitted to the system.",
    responses={
        200: {"description": "List of all adoption applications"}
    }
)
async def get_adoption_applications(session: SessionDep):
    applications = session.exec(select(AdoptionApplication)).all()
    return {"applications": applications}

@router.delete(
    "/{application_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete adoption application",
    description="Permanently delete an adoption application from the system. This action cannot be undone.",
    responses={
        200: {"description": "Application deleted successfully"},
        404: {"description": "Application not found"}
    }
)
async def delete_adoption_application(application_id: int, session: SessionDep):
    application = session.get(AdoptionApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    session.delete(application)
    session.commit()
    return {"success": "Adoption application deleted successfully"}