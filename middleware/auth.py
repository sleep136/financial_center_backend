# # middleware/auth.py
# from fastapi import Request, HTTPException, status
# from jose import JWTError, jwt
# from typing import List, Set
# import re
#
#
# class GroupPermissionMiddleware:
#     def __init__(self, secret_key: str):
#         self.secret_key = secret_key
#
#     def get_user_permissions(self, group_ids: List[int]) -> Set[str]:
#         """根据group_id获取权限列表"""
#         permissions = set()
#
#         for group_id in group_ids:
#             if group_id in GROUP_PERMISSIONS:
#                 group_perms = GROUP_PERMISSIONS[group_id]["permissions"]
#                 if "*" in group_perms:
#                     return {"*"}  # 拥有所有权限
#                 permissions.update(group_perms)
#
#         # 如果没有group_id，使用会计权限
#         if not group_ids:
#             permissions.update(NO_GROUP_PERMISSIONS["permissions"])
#
#         return permissions
#
#     def has_permission(self, request_path: str, user_permissions: Set[str]) -> bool:
#         """检查用户是否有访问路径的权限"""
#         if "*" in user_permissions:
#             return True
#
#         for pattern in user_permissions:
#             # 简单的路径匹配，支持通配符
#             if pattern.endswith("*"):
#                 if request_path.startswith(pattern.rstrip("*")):
#                     return True
#             elif request_path == pattern:
#                 return True
#
#         return False
#
#     async def __call__(self, request: Request, call_next):
#         # 公开路径（不需要权限检查）
#         public_paths = [
#             "/api/auth/login",
#             "/api/auth/refresh",
#             "/docs",
#             "/openapi.json"
#         ]
#
#         if request.url.path in public_paths or \
#                 request.url.path.startswith("/static/"):
#             return await call_next(request)
#
#         # 获取token
#         auth_header = request.headers.get("Authorization")
#         if not auth_header:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="未提供认证令牌"
#             )
#
#         try:
#             token = auth_header.split(" ")[1]
#             payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
#
#             # 提取用户信息和权限
#             user_groups = payload.get("groups", [])
#             user_permissions = self.get_user_permissions(user_groups)
#
#             # 将权限信息存入request.state
#             request.state.user_id = payload.get("sub")
#             request.state.groups = user_groups
#             request.state.permissions = list(user_permissions)
#             request.state.is_admin = 1 in user_groups
#             request.state.is_accountant = (3 in user_groups) or (not user_groups)
#
#             # 检查当前路径权限
#             if not self.has_permission(request.url.path, user_permissions):
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="无权访问该页面"
#                 )
#
#         except JWTError:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="无效的认证令牌"
#             )
#
#         return await call_next(request)