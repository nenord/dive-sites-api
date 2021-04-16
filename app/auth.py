from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from typing import Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from .crud import check_user_name

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "ba503476f568da5f622e3ea9191bebc5664c7eb8fe02e99e1ce1768ba8a7b6bb"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=5)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_username: str = payload.get("sub")
        if token_username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = check_user_name(token_username)
    if user is None:
        raise credentials_exception
    return user