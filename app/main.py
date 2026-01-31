from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import animals, volunteer, contact, adopt, users
from app.cloudinary.routers import media
from app.internal import admin
from app.database import create_db_and_tables

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


app.include_router(animals.router)
app.include_router(volunteer.router)
app.include_router(contact.router)
app.include_router(adopt.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(media.router)