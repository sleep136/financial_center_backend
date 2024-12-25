from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from passlib.context import CryptContext
from db import user_engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)
    password: Optional[str] = Field(default=None)

    class Meta:
        table_name = "auth_user"


def get_user_by_name(username: str):
    with Session(user_engine) as session:
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        if results:
            return results[0]


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
