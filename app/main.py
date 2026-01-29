from fastapi import FastAPI
from app.routers import animals, volunteer, contact, adopt, users
from app.cloudinary.routers import media
from app.internal import admin
from app.database import create_db_and_tables
from app import auth

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


app.include_router(animals.router)
app.include_router(volunteer.router)
app.include_router(contact.router)
app.include_router(adopt.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(media.router)