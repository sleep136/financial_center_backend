from http.client import HTTPException

from fastapi import APIRouter, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from  service.user import authenticate
from dependencies import Token
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
import jwt
router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = authenticate(form_data.username, form_data.password, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
