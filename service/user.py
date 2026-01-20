from datetime import datetime, timedelta

import jwt

from models.User import get_user_by_name, verify_password, get_user_group

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 权限配置
GROUP_PERMISSIONS = {
    1: {  # 管理员
        "name": "admin",
        "description": "管理员权限",
        "permissions": ["*"]  # 所有权限
    },
    2: {  # 后台权限
        "name": "backend",
        "description": "后台权限",
        "permissions": ["*"]  # 目前所有权限
    },
    3: {  # 会计权限
        "name": "accountant",
        "description": "会计权限",
        "permissions": [

            "/indicator",  # 报表页面

        ]
    }
}

# 如果没有group_id（会计权限）
NO_GROUP_PERMISSIONS = {
    "name": "accountant_no_group",
    "description": "会计权限（无group_id）",
    "permissions": [
        "/indicator",

    ]
}


def authenticate(username, password):
    user = get_user_by_name(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_user_info(username, password):
    user = authenticate(username, password)
    if not user:
        return False

    user_groups = get_user_group(user.id)
    # 生成token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "groups": user_groups,
            "is_admin": 1 in user_groups,
            "is_accountant": (3 in user_groups) or (not user_groups)
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "groups": user_groups,
            "permissions": get_user_permissions(user_groups)
        }
    }





def get_user_permissions(group_ids):
    """获取用户权限列表（用于返回给前端）"""
    permissions = set()

    for group_id in group_ids:
        if group_id in GROUP_PERMISSIONS:
            perms = GROUP_PERMISSIONS[group_id]["permissions"]
            if "*" in perms:
                return ["*"]
            permissions.update(perms)

    if not group_ids:
        permissions.update(NO_GROUP_PERMISSIONS["permissions"])

    return list(permissions)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
