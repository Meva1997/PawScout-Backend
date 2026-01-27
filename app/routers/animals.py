from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, Field, select
from app.database import SessionDep

router = APIRouter()

class Animal(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True) # add index for faster searches 
    type: str = Field(index=True)
    age: int
    gender: str
    size: str
    breed: str
    shortDescription: str
    longDescription: str
    goodWithKids: bool
    goodWithDogs: bool
    homeTrained: bool
    availableForAdoption: str 



@router.get("/animals")
async def read_animals(session: SessionDep):
    animals = session.exec(select(Animal)).all()
    return {"animals": animals}


@router.get("/animals/{animal_id}")
async def read_animal(animal_id: int, session: SessionDep):
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal


@router.post("/animals")
async def create_animal(animal: Animal, session: SessionDep): 

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

@router.put("/animals/{animal_id}")
async def update_animal(animal_id: int, updated_animal: Animal, session: SessionDep):
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

@router.delete("/animals/{animal_id}")
async def delete_animal(animal_id: int, session: SessionDep):
    animal = session.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")

    session.delete(animal)
    session.commit()

    return {"success": "Animal deleted successfully"}