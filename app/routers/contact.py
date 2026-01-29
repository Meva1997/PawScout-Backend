from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, select
from app.database import SessionDep
 
router = APIRouter(
    prefix="/contact",
    tags=["contact"],
)

class ContactMessage(SQLModel, table=True):
    """Contact form message model for user inquiries and feedback."""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100, description="Sender's first name")
    lastName: str = Field(min_length=1, max_length=100, description="Sender's last name")
    email: EmailStr = Field(description="Sender's email address")
    subject: str = Field(min_length=3, max_length=200, description="Message subject")
    message: str = Field(min_length=10, max_length=2000, description="Message content")
    date: str = Field(description="Message submission date")



@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Send contact message",
    description="Submit a contact form message. All fields are required and will be validated.",
    responses={
        201: {"description": "Contact message sent successfully"},
        400: {"description": "Invalid input - empty fields or validation errors"}
    }
)
async def send_contact_message(contact_message: ContactMessage, session: SessionDep):
    for field, value in contact_message.dict().items():
        if field == "id":
            continue

        if isinstance(value, str) and value.strip() == "":
                raise HTTPException(status_code=400, detail=f"{field} cannot be empty")

    session.add(contact_message)
    session.commit()
    session.refresh(contact_message)
    return {"success": "Contact message sent successfully"}

@router.get(
    "/{message_id}",
    status_code=status.HTTP_200_OK,
    summary="Get contact message by ID",
    description="Retrieve a specific contact message by its ID.",
    responses={
        200: {"description": "Contact message found"},
        404: {"description": "Contact message not found"}
    }
)
async def get_contact_message(message_id: int, session: SessionDep):
    contact_message = session.get(ContactMessage, message_id)
    if not contact_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    return contact_message

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get all contact messages",
    description="Retrieve all contact messages submitted through the contact form.",
    responses={
        200: {"description": "List of all contact messages"}
    }
)
async def get_all_contact_messages(session: SessionDep):
    messages = session.exec(select(ContactMessage)).all()
    return {"contact_messages": messages}

@router.delete(
    "/{message_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete contact message",
    description="Permanently delete a contact message from the system. This action cannot be undone.",
    responses={
        200: {"description": "Contact message deleted successfully"},
        404: {"description": "Contact message not found"}
    }
)
async def delete_contact_message(message_id: int, session: SessionDep):
    contact_message = session.get(ContactMessage, message_id)
    if not contact_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    session.delete(contact_message)
    session.commit()
    return {"success": "Contact message deleted successfully"}