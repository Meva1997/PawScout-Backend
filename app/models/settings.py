from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


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


class ShelterSettingsUpdate(BaseModel):
    """Model for updating shelter settings."""
    shelter_name: Optional[str] = Field(default=None, max_length=200)
    shelter_email: Optional[EmailStr] = None
    shelter_phone: Optional[str] = Field(default=None, max_length=50)
    shelter_address: Optional[str] = Field(default=None, max_length=500)
    city: Optional[str] = Field(default=None, max_length=100)
    state: Optional[str] = Field(default=None, max_length=100)
    zip_code: Optional[str] = Field(default=None, max_length=20)
    
    class Config:
        json_schema_extra = {
            "example": {
                "logo_url": "https://res.cloudinary.com/example/image/upload/v123/logo.png",
                "logo_public_id": "pawscout/settings/logo_abc123",
                "shelter_name": "PawScout Animal Shelter",
                "shelter_email": "info@pawscout.com",
                "shelter_phone": "+1-555-0123",
                "shelter_address": "123 Main Street, City, State 12345"
            }
        }
 