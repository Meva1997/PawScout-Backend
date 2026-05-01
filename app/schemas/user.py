from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login credentials schema."""

    email: EmailStr = Field(description="User's email address")
    password: str = Field(min_length=1, description="User's password")
