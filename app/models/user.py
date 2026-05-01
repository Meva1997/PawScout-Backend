from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class PawUser(SQLModel, table=True):
    """User model for authentication and authorization."""

    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True, description="User's email address")
    name: str = Field(min_length=1, max_length=100, description="User's first name")
    lastName: str = Field(min_length=1, max_length=100, description="User's last name")
    password: str = Field(min_length=8, description="Hashed password")
    isAdmin: bool = Field(default=False, description="Whether user has admin privileges")
