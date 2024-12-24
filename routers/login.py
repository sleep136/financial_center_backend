
from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from  models import User
router = APIRouter()

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = authenticate_user(users_db, form_data.username, form_data.password, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "JWT"})


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
