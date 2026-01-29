from typing import Annotated, TYPE_CHECKING
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select
from app.auth import SECRET_KEY, ALGORITHM
from app.database import get_session

if TYPE_CHECKING:
    from app.routers.users import PawUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: TokenDep, session: SessionDep) -> "PawUser":
    """
    Dependency to get the current authenticated user from JWT token.
    Validates token and retrieves user from database.
    """
    # Import here to avoid circular import
    from app.routers.users import PawUser
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            raise credentials_exception
            
    except InvalidTokenError:
        raise credentials_exception
    
    # Get user from database
    user = session.get(PawUser, user_id)
    if user is None:
        raise credentials_exception
        
    return user


async def get_current_admin_user(
    current_user: Annotated["PawUser", Depends(get_current_user)]
) -> "PawUser":
    """
    Dependency to verify that the current user has admin privileges.
    Use this to protect admin-only endpoints.
    """
    if not current_user.isAdmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource. Admin privileges required."
        )
    return current_user


# Type aliases for cleaner route definitions
CurrentUser = Annotated["PawUser", Depends(get_current_user)]
AdminUser = Annotated["PawUser", Depends(get_current_admin_user)]
