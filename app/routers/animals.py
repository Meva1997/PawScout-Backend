from fastapi import APIRouter, HTTPException, status
from sqlmodel import SQLModel, Field, select
from sqlalchemy import Column, String, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from typing import List
from enum import Enum
from app.database import SessionDep
from app.dependencies import AdminUser


class AnimalStatus(str, Enum):
    """Status options for animal adoption availability."""
    available = "available"
    pending = "pending"
    adopted = "adopted"

class Animal(SQLModel, table=True):
    """Animal model for adoption listings."""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=1, max_length=100, description="Animal's name")
    type: str = Field(index=True, min_length=1, max_length=50, description="Animal type (e.g., dog, cat)")
    age: int = Field(ge=0, le=30, description="Animal's age in years")
    gender: str = Field(min_length=1, max_length=20, description="Animal's gender")
    size: str = Field(min_length=1, max_length=20, description="Animal's size (small, medium, large)")
    breed: str = Field(min_length=1, max_length=100, description="Animal's breed")
    shortDescription: str = Field(min_length=1, max_length=200, description="Brief description")
    longDescription: str = Field(min_length=1, max_length=2000, description="Detailed description")
    goodWithKids: bool = Field(description="Whether animal is good with children")
    goodWithDogs: bool = Field(description="Whether animal is good with other dogs")
    homeTrained: bool = Field(description="Whether animal is house trained")
    availableForAdoption: AnimalStatus = Field(default=AnimalStatus.available, description="Adoption availability status")
    media: List[dict] | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Array of media objects with url, public_id, and resource_type (image/video)"
    )

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