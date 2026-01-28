from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, Field, select
from app.database import SessionDep
from app.routers.animals import Animal



router = APIRouter()


class AdoptionApplication(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    animalId: int = Field(foreign_key="animal.id", index=True)
    applicantName: str
    applicantLastName: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zipCode: str
    reasonForAdoption: str
    experienceWithPets: str
    homeType: str 
    whoLivesInHouse: str
    agreeToTerms: bool
    date: str


@router.post("/adopt/{animal_id}", status_code=201)
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


@router.get("/adopt/{application_id}")
async def get_adoption_application(application_id: int, session: SessionDep):
    application = session.get(AdoptionApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.get("/adopt")
async def get_adoption_applications(session: SessionDep):
    applications = session.exec(select(AdoptionApplication)).all()
    return {"applications": applications}

@router.delete("/adopt/{application_id}")
async def delete_adoption_application(application_id: int, session: SessionDep):
    application = session.get(AdoptionApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    session.delete(application)
    session.commit()
    return {"success": "Adoption application deleted successfully"}