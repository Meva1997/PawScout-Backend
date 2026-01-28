from typing import Annotated
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
from fastapi import Depends
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables")

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Ensure all SQLModel tables exist before serving requests."""
    from app.routers.animals import Animal  # noqa: F401
    from app.routers.adopt import AdoptionApplication  # noqa: F401
    from app.routers.volunteer import Volunteer  # noqa: F401
    from app.routers.contact import ContactMessage  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
