from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, select
from app.database import SessionDep
 
router = APIRouter()

class ContactMessage(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    lastName: str
    email: str
    subject: str
    message: str
    date: str



@router.post("/contact")
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

@router.get("/contact/{message_id}")
async def get_contact_message(message_id: int, session: SessionDep):
    contact_message = session.get(ContactMessage, message_id)
    if not contact_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    return contact_message

@router.get("/contact")
async def get_all_contact_messages(session: SessionDep):
    messages = session.exec(select(ContactMessage)).all()
    return {"contact_messages": messages}

@router.delete("/contact/{message_id}")
async def delete_contact_message(message_id: int, session: SessionDep):
    contact_message = session.get(ContactMessage, message_id)
    if not contact_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    session.delete(contact_message)
    session.commit()
    return {"success": "Contact message deleted successfully"}