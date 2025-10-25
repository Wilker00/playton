"""Authentication and authorization utilities for the trading platform."""

from datetime import UTC, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from backend.settings import get_settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


class Token(BaseModel):
    """Access token response payload."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token payload data."""

    username: Optional[str] = None
    role: str = "viewer"


class User(BaseModel):
    """User account representation."""

    username: str
    disabled: bool = False
    role: str = "viewer"


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """Issue a signed JWT for the provided credentials."""

    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": form_data.username, "role": form_data.scopes[0] if form_data.scopes else "viewer", "exp": expire}
    encoded_jwt = jwt.encode(payload, settings.secret_key, algorithm="HS256")
    return Token(access_token=encoded_jwt, expires_in=settings.access_token_expire_minutes * 60)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Validate the token and return the associated user."""

    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        role: str = payload.get("role", "viewer")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return User(username=username, role=role)
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token validation failed") from exc
