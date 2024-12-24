from http.client import HTTPException

from fastapi import APIRouter, status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from  service.user import authenticate
router = APIRouter()

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


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
