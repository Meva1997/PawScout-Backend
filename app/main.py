from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import adopt, admin, animals, contact, media, subs, users, volunteer

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite dev server
]

# Add production frontend URL if available
if settings.FRONTEND_URL:
    origins.append(settings.FRONTEND_URL)
    # Also add without trailing slash if it has one
    if settings.FRONTEND_URL.endswith("/"):
        origins.append(settings.FRONTEND_URL.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(animals.router)
app.include_router(volunteer.router)
app.include_router(contact.router)
app.include_router(adopt.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(media.router)
app.include_router(subs.router)
