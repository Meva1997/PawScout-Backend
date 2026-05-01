from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ShelterSettings(SQLModel, table=True):
    """Model to store shelter configuration and settings."""

    __tablename__ = "shelter_settings"

    id: Optional[int] = Field(default=None, primary_key=True)
    logo_url: Optional[str] = Field(default=None, description="URL of the shelter logo on Cloudinary")
    logo_public_id: Optional[str] = Field(default=None, description="Cloudinary public_id for logo management")
    shelter_name: Optional[str] = Field(default="PawScout Shelter", max_length=200)
    shelter_email: Optional[str] = Field(default=None, max_length=200)
    shelter_phone: Optional[str] = Field(default=None, max_length=50)
    shelter_address: Optional[str] = Field(default=None, max_length=500)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    zip_code: Optional[str] = Field(default=None, max_length=20)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
