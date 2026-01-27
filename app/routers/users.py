from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

#Router for user logins and registrations
mock_users = [
    {
        "id": 1,
        "email": "johndoe@example.com",
        "name": "John",
        "lastName": "Doe",
        "password": "password"
    },
    {
        "id": 2,
        "email": "janedoe@example.com",
        "name": "Jane",
        "lastName": "Doe",
        "password": "password"
    }
]

class User(BaseModel):
    id: int
    email: str
    name: str
    lastName: str
    password: str
    isAdmin: bool = False

@router.post("/users/register")
async def register_user(user: User):
    # In a real application, you would save the user to a database here
    return {"status": "User registered", "user": user}

@router.post("/users/login")
async def login_user(email: str, password: str):
    for user in mock_users:
        if user["email"] == email and user["password"] == password:
            return {"status": "Login successful", "user": user}
    raise HTTPException(status_code=401, detail="Invalid email or password")

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    for user in mock_users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")