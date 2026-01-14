import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from db import  create_db_and_tables
from routers import login,program,student,authorization,approval_workflow

app = FastAPI()
# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:57587",  # 前端开发服务器
        "http://127.0.0.1:57587",
        "http://127.0.0.1:80",
        "http://172.31.22.3",
        "http://localhost:5173",   # Vite 默认端口
        "http://localhost:8080",   # Vue CLI 默认端口
        "http://172.31.22.3",  # Nginx地址
        "http://localhost",     # 本地访问
        "http://127.0.0.1",    # 本地回环
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

from utils.logging import create_logger
create_logger()
import logging
logger = logging.getLogger('financial_center_backend.app')

app.include_router(login.router)
app.include_router(program.router)
app.include_router(student.router)
app.include_router(authorization.router)
app.include_router(approval_workflow.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
