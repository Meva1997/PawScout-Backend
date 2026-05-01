from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.database import SessionDep
from app.models import Subscription

router = APIRouter(
    prefix="/subs",
    tags=["subs"],
)


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
