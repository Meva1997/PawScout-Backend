from enum import Enum
from typing import List

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


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
    availableForAdoption: AnimalStatus = Field(
        default=AnimalStatus.available, description="Adoption availability status"
    )
    media: List[dict] | None = Field(
        default=None,
        sa_column=Column(JSON),
        description="Array of media objects with url, public_id, and resource_type (image/video)",
    )
