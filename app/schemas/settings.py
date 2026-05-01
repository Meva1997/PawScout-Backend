from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ShelterSettingsUpdate(BaseModel):
    """Schema for updating shelter settings."""

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
                "shelter_address": "123 Main Street, City, State 12345",
            }
        }
