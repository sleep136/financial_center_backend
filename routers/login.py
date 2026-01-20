
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter,HTTPException

from service.user import get_user_info, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import JWTError, jwt
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


class LoginData(BaseModel):
    """登录请求数据模型"""
    username: str
    password: str


@router.post("/login")
async def login(
        login_data: LoginData

):
    """用户登录"""
    user = get_user_info(login_data.username, login_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    # 生成token

    return user


@router.get("/login/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        groups: list = payload.get("groups", [])

        if user_id is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭证",
            )

        return {
            "id": int(user_id),
            "username": username,
            "groups": groups,
            "is_admin": 1 in groups,
            "is_accountant": (3 in groups) or (len(groups) == 0)
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
        )


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
