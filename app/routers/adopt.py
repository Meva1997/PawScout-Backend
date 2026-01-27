from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, Field
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


@router.post("/adopt/{animal_id}", status_code=201)
async def submit_adoption_application(
    animal_id: int, application: AdoptionApplication, session: SessionDep
):

    for field, value in application.dict().items():
        if field == "id" and field == "animalId":
            continue

        if isinstance(value, str) and value.strip() == "":
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

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