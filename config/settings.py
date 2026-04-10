from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 基础配置
    app_name: str = "My FastAPI App"
    debug: bool = False

    # 数据库配置
    database_url: str = "postgresql://user:password@localhost/dbname"
    database_pool_size: int = 20

    # # Redis配置
    # redis_url: str = "redis://localhost:6379/0"
    # Redis
    REDIS_URL: str = "redis://172.31.22.3:6379/0"
    # 要检查的服务列表（IP:端口）
    TARGET_SERVICES: dict = {
        "172.31.22.185:8080": "财务-劳务申报系统",
        "172.31.22.185:80": "财务-服务大厅",
        "172.31.22.185:8051": "智慧平台",
        # "172.31.22.118:8080/workFlowWB/": "审批平台",
        # "172.31.22.185:8051": "智慧平台",
        # "172.31.22.185:8051": "智慧平台",
        # "172.31.22.185:8051": "智慧平台",

    }
    # 定时检查间隔（秒）
    CHECK_INTERVAL: int = 1200
    #
    # # JWT配置
    # secret_key: str = "your-secret-key"
    # algorithm: str = "HS256"
    # access_token_expire_minutes: int = 30

    # 外部API配置
    external_api_key: Optional[str] = None
    external_api_url: str = "https://api.example.com"

    # CORS配置
    cors_origins: list = ["http://localhost:8000", "https://yourdomain.com"]

    # 环境变量文件
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False


settings = Settings()
