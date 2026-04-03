from fastapi import APIRouter
from config.settings import settings
from utils.scheduler import start_scheduler,scheduler
from utils.health_checker import redis

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 启动时自动开启定时任务
@router.on_event("startup")
async def startup_event():
    start_scheduler()

@router.on_event("shutdown")
async def shutdown_event():
    if scheduler.running:
        scheduler.shutdown(wait=False)

# API：获取所有服务的健康状态
@router.get("/health/all")
def get_all_health():
    result = {}
    for service in settings.TARGET_SERVICES:
        data = redis.hgetall(f"health:{service}")
        result[service] = data
    return {"services": result}