from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from typing import Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os

from .crud import get_user
from .schemas import User_out

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
EXPIRE_TOKEN = os.environ.get("EXPIRE_TOKEN")

def create_access_token(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(EXPIRE_TOKEN))
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
        token_id: str = payload.get("sub")
        if token_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(token_id)
    if user is None:
        raise credentials_exception
    return User_out(**user)