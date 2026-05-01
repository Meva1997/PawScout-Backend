from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.security import ALGORITHM, SECRET_KEY
from app.database import get_session
from app.models import PawUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep, session: SessionDep) -> PawUser:
    """Decode the JWT and load the corresponding PawUser from the database."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if email is None or user_id is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = session.get(PawUser, user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_admin_user(
    current_user: Annotated[PawUser, Depends(get_current_user)],
) -> PawUser:
    """Ensure the current user has admin privileges."""
    if not current_user.isAdmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource. Admin privileges required.",
        )
    return current_user


CurrentUser = Annotated[PawUser, Depends(get_current_user)]
AdminUser = Annotated[PawUser, Depends(get_current_admin_user)]
