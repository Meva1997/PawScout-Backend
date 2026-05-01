from sqlmodel import Field, SQLModel


class Subscription(SQLModel, table=True):
    """Newsletter subscription model."""

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(min_length=1, max_length=100, description="Subscriber's email address")
