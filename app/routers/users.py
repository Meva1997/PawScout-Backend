from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field as PydanticField
from sqlmodel import SQLModel, Field, select
from app.database import SessionDep
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.dependencies import CurrentUser

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

class PawUser(SQLModel, table=True):
    """User model for authentication and authorization."""
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True, description="User's email address")
    name: str = Field(min_length=1, max_length=100, description="User's first name")
    lastName: str = Field(min_length=1, max_length=100, description="User's last name")
    password: str = Field(min_length=8, description="Hashed password")
    isAdmin: bool = Field(default=False, description="Whether user has admin privileges")


class LoginRequest(BaseModel):
    """Login credentials schema."""
    email: EmailStr = PydanticField(description="User's email address")
    password: str = PydanticField(min_length=1, description="User's password")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password. Password will be hashed before storage.",
    responses={
        201: {"description": "User registered successfully"},
        400: {"description": "Invalid input data (empty fields or password too short)"},
        409: {"description": "Email already registered"}
    }
)
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

    

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and get access token",
    description="Login with email and password. Returns a JWT token valid for 30 minutes with user claims including admin status.",
    responses={
        200: {"description": "Login successful, returns access token and user data"},
        400: {"description": "Email or password cannot be empty"},
        401: {"description": "Invalid email or password"}
    }
)
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


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user",
    description="Get the current user's information from the JWT token. Requires valid Bearer token in Authorization header.",
    responses={
        200: {"description": "Current user information"},
        401: {"description": "Invalid or expired token"},
    }
)
async def get_current_user_info(current_user: CurrentUser):
    """Get current authenticated user information from JWT token."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "lastName": current_user.lastName,
        "isAdmin": current_user.isAdmin
    }


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Retrieve user information by user ID. Password is excluded for security.",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"}
    }
)
async def get_user(user_id: int, session: SessionDep):
    user = session.get(PawUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return user without password
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "lastName": user.lastName,
        "isAdmin": user.isAdmin
    }