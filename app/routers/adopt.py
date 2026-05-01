from fastapi import APIRouter, Body, HTTPException, status
from sqlmodel import select

from app.core.deps import AdminUser
from app.database import SessionDep
from app.models import AdoptionApplication, AdoptionStatus, Animal, AnimalStatus

router = APIRouter(
    prefix="/adopt",
    tags=["adopt"],
)


@router.post(
    "/{animal_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Submit adoption application",
    description="Submit an adoption application for a specific animal. The animal's status will be updated to 'pending'. All fields must be provided and validated.",
    responses={
        201: {"description": "Adoption application submitted successfully"},
        400: {"description": "Invalid input - empty fields or validation errors"},
        404: {"description": "Animal not found"},
        409: {"description": "Animal already in adoption process (pending or approved)"}
    }
)
async def submit_adoption_application(
    animal_id: int, application: AdoptionApplication, session: SessionDep
):

    #verify if animal exists with the given animal_id
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    if animal.availableForAdoption in [AnimalStatus.pending, AnimalStatus.adopted]:
        raise HTTPException(status_code=409, detail="Animal is already in adoption process")

    for field, value in application.dict().items():
        if field in ["id", "animalId", "status"]:
            continue

        if isinstance(value, str) and value.strip() == "":
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

    # Set animal status to pending
    animal.availableForAdoption = AdoptionStatus.pending
    session.add(animal)

    application.status = AdoptionStatus.pending
    session.add(application)
    session.commit()
    session.refresh(application)
    return {"success": "Adoption application submitted successfully"}


@router.get(
    "/{application_id}",
    status_code=status.HTTP_200_OK,
    summary="Get adoption application by ID",
    description="Retrieve details of a specific adoption application. Requires admin privileges.",
    responses={
        200: {"description": "Application found"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"},
        404: {"description": "Application not found"}
    }
)
async def get_adoption_application(application_id: int, session: SessionDep, admin: AdminUser):
    application = session.get(AdoptionApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all adoption applications",
    description="Retrieve a list of all adoption applications submitted to the system. Requires admin privileges.",
    responses={
        200: {"description": "List of all adoption applications"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"}
    }
)
async def get_adoption_applications(session: SessionDep, admin: AdminUser):
    applications = session.exec(select(AdoptionApplication)).all()
    return {"applications": applications}

@router.delete(
    "/{application_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete adoption application",
    description="Permanently delete an adoption application from the system. This action cannot be undone. Requires admin privileges.",
    responses={
        200: {"description": "Application deleted successfully"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"},
        404: {"description": "Application not found"}
    }
)
async def delete_adoption_application(application_id: int, session: SessionDep, admin: AdminUser):
    application = session.get(AdoptionApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Check if the application was rejected or pending before deleting, if so set the animal's status back to available
    if application.status in [AdoptionStatus.rejected, AdoptionStatus.pending]:
        animal = session.get(Animal, application.animalId)
        if animal:
            animal.availableForAdoption = AnimalStatus.available
            session.add(animal)

    session.delete(application)
    session.commit()
    return {"success": "Adoption application deleted successfully"}

@router.put(
    "/{application_id}/status",
    status_code=status.HTTP_200_OK,
    summary="Update adoption application status",
    description="Update the status of an adoption application (approved, pending, rejected). Requires admin privileges.",
    responses={
        200: {"description": "Application status updated successfully"},
        400: {"description": "Invalid input - empty fields or validation errors"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"},
        404: {"description": "Application not found"}
    }
)
async def update_adoption_application_status(
    application_id: int,
    new_status: AdoptionStatus = Body(..., embed=True, alias="status"),
    session: SessionDep = None,
    admin: AdminUser = None,
):
    application = session.get(AdoptionApplication, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    animal = session.get(Animal, application.animalId)
    if not animal:
        raise HTTPException(status_code=404, detail="Associated animal not found")

    application.status = new_status

    if new_status == AdoptionStatus.approved:
        animal.availableForAdoption = AnimalStatus.adopted
    elif new_status == AdoptionStatus.pending:
        animal.availableForAdoption = AnimalStatus.pending
    elif new_status == AdoptionStatus.rejected:
        animal.availableForAdoption = AnimalStatus.available

    session.add(application)
    session.add(animal)
    session.commit()
    session.refresh(application)

    return {"success": "Adoption application status updated successfully"}
