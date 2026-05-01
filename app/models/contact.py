from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class ContactMessage(SQLModel, table=True):
    """Contact form message model for user inquiries and feedback."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100, description="Sender's first name")
    lastName: str = Field(min_length=1, max_length=100, description="Sender's last name")
    email: EmailStr = Field(description="Sender's email address")
    subject: str = Field(min_length=3, max_length=200, description="Message subject")
    message: str = Field(min_length=10, max_length=2000, description="Message content")
    date: str = Field(description="Message submission date")
