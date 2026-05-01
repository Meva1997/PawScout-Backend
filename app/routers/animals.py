from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.core.deps import AdminUser
from app.database import SessionDep
from app.models import Animal

router = APIRouter(
    prefix="/animals",
    tags=["animals"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all animals",
    description="Retrieve a list of all animals available for adoption, including those pending or already adopted.",
    responses={
        200: {"description": "List of all animals"}
    }
)
async def read_animals(session: SessionDep):
    animals = session.exec(select(Animal)).all()
    return {"animals": animals}


@router.get(
    "/{animal_id}",
    status_code=status.HTTP_200_OK,
    summary="Get animal by ID",
    description="Retrieve detailed information about a specific animal by its ID.",
    responses={
        200: {"description": "Animal found"},
        404: {"description": "Animal not found"}
    }
)
async def read_animal(animal_id: int, session: SessionDep):
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new animal listing",
    description="Add a new animal to the adoption system. All fields except 'id' and 'availableForAdoption' are required. Requires admin privileges.",
    responses={
        201: {"description": "Animal created successfully"},
        400: {"description": "Invalid input - empty fields or validation errors"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"}
    }
)
async def create_animal(animal: Animal, session: SessionDep, admin: AdminUser):

    for field, value in animal.dict().items():
        if field == "id":
            continue

        if field == "availableForAdoption":
            continue

        if isinstance(value, str) and value.strip() == "":
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

    session.add(animal)
    session.commit()
    session.refresh(animal)

    return {"success": "Animal created successfully"}

@router.put(
    "/{animal_id}",
    status_code=status.HTTP_200_OK,
    summary="Update an existing animal",
    description="Update all information for an existing animal. Requires all fields to be provided. Requires admin privileges.",
    responses={
        200: {"description": "Animal updated successfully"},
        400: {"description": "Invalid input - empty fields or validation errors"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"},
        404: {"description": "Animal not found"}
    }
)
async def update_animal(animal_id: int, updated_animal: Animal, session: SessionDep, admin: AdminUser):
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    for field, value in updated_animal.dict().items():
        if field == "id":
            continue

        if isinstance(value, str) and value.strip() == "":
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

        setattr(animal, field, value)

    session.add(animal)
    session.commit()
    session.refresh(animal)

    return {"success": "Animal updated successfully"}

@router.delete(
    "/{animal_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an animal",
    description="Permanently remove an animal from the system. This action cannot be undone. Requires admin privileges.",
    responses={
        200: {"description": "Animal deleted successfully"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        403: {"description": "Forbidden - Admin privileges required"},
        404: {"description": "Animal not found"}
    }
)
async def delete_animal(animal_id: int, session: SessionDep, admin: AdminUser):
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    session.delete(animal)
    session.commit()

    return {"success": "Animal deleted successfully"}
