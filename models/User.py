from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, List
from passlib.context import CryptContext
from db import user_engine
import base64
import hashlib
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUserGroups(SQLModel, table=True):
    __tablename__ = "auth_user_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    group_id: int


class User(SQLModel, table=True):
    __tablename__ = "auth_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=True)
    password: Optional[str] = Field(default=None)


def get_user_by_name(username: str) -> Optional[User]:
    with Session(user_engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        return user


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return password_verify(password, hashed_password)


def password_encrypt(password, salt=None, iterations=150000):
    """
    密码加密:PBKDF2_SHA256加密
    加密格式：pbkdf2_sha256$迭代次数$盐$哈希值
    """
    salt = salt or base64.b64encode(os.urandom(16)).decode('utf-8')
    hash_object = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
    hash_value_b64 = base64.b64encode(hash_object).decode('utf-8')
    encrypted_string = f'pbkdf2_sha256${iterations}${salt}${hash_value_b64}'
    return encrypted_string


def password_verify(password, encrypted_string):
    """
    密码验证:PBKDF2_SHA256加密
    """
    try:
        parts = encrypted_string.split('$')
        if len(parts) < 4:
            return False
        iterations, salt, hash_value_b64 = parts[-3:]
        return password_encrypt(password, salt, int(iterations)) == encrypted_string
    except:
        return False


def get_user_by_id(user_id: int) -> Optional[User]:
    with Session(user_engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user


def get_user_group(user_id: int) -> List[int]:
    """获取用户的group_id列表"""
    with Session(user_engine) as session:
        statement = select(AuthUserGroups.group_id).where(AuthUserGroups.user_id == user_id)
        results = session.exec(statement)
        return [row for row in results]


def get_user_info_with_groups(username: str) -> Optional[dict]:
    """获取用户信息和group_id列表"""
    user = get_user_by_name(username)
    if not user:
        return None

    groups = get_user_group(user.id)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "is_active": user.is_active,
        "groups": groups,
        "is_admin": 1 in groups,
        "is_accountant": (3 in groups) or (len(groups) == 0)
    }