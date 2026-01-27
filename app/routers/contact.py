from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ContactMessage(BaseModel):
    name: str
    lastName: str
    email: str
    subject: str
    message: str

@router.post("/contact")
async def send_contact_message(contact_message: ContactMessage):
    # In a real application, you would process the contact message here
    return {"status": "Message received", "message": contact_message}