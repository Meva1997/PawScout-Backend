from fastapi import APIRouter, HTTPException, status
from sqlmodel import SQLModel, Field, select
from app.database import SessionDep 


router = APIRouter(
    prefix="/subs",
    tags=["subs"],
)

class Subscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(min_length=1, max_length=100, description="Subscriber's email address")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Subscribe to newsletter",
    description="Submit an email address to subscribe to the shelter's newsletter. The email will be validated and stored in the database.",
    responses={
        201: {"description": "Subscription successful"},
        400: {"description": "Invalid input - empty email or validation errors"}
    }
)
async def subscribe(subscription: Subscription, session: SessionDep):
    if subscription.email.strip() == "":
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    session.add(subscription)
    session.commit()
    session.refresh(subscription)
    return {"success": "Subscription successful"}


@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  summary="Get all subscriptions",
  description="Retrieve a list of all newsletter subscriptions",
  responses={
    200: {"description": "List of subscriptions retrieved successfully"},
    404: {"description": "No subscriptions found"}
  }
)
async def get_subscriptions(session: SessionDep):
    subscriptions = session.exec(select(Subscription)).all()
    if not subscriptions:
        raise HTTPException(status_code=404, detail="No subscriptions found")
    return subscriptions