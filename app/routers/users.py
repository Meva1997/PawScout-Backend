from datetime import timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, select
from app.database import SessionDep
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

class PawUser(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    name: str
    lastName: str
    password: str
    isAdmin: bool = False


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register_user(paw_user: PawUser, session: SessionDep):
    existing_user = session.exec(select(PawUser).where(PawUser.email == paw_user.email)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    for field, value in paw_user.dict().items():
        if field == "id" or field == "isAdmin":
            continue

        if isinstance(value, str) and value.strip() == "":
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

    # Hash the password before storing it in the database
    paw_user.password = get_password_hash(paw_user.password)

    session.add(paw_user)
    session.commit()
    session.refresh(paw_user)
    return {"success": "User registered successfully"}

    

@router.post("/login")
async def login_user(credentials: LoginRequest, session: SessionDep):
    # Validate credentials are not empty
    if not credentials.email.strip() or not credentials.password.strip():
        raise HTTPException(status_code=400, detail="Email and password cannot be empty")
    
    # Find user by email
    db_user = session.exec(select(PawUser).where(PawUser.email == credentials.email)).first()
    
    # Verify user exists and password matches using secure hash comparison
    if not db_user or not verify_password(credentials.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Generate JWT token with user info including admin status
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": db_user.email,  # Subject: user identifier
            "user_id": db_user.id,
            "isAdmin": db_user.isAdmin,
            "name": db_user.name,
            "lastName": db_user.lastName
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, # the JWT token contains the isAdmin claim
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "lastName": db_user.lastName,
            "isAdmin": db_user.isAdmin
        }
    }

@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep):
    user = session.get(PawUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user