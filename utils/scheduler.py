from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.health_checker import run_all_health_checks
from config.settings import settings

# 全局唯一调度器
scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")

def start_scheduler():
    """
    终极安全启动：解决热重载 / 重启导致的重复启动报错
    """
    # 👇 最关键：只检查状态，不强行关闭，避免异步冲突
    if scheduler.running:
        print("调度器已在运行，跳过启动")
        return

    # 添加任务
    scheduler.add_job(
        run_all_health_checks,
        trigger="interval",
        seconds=settings.CHECK_INTERVAL,
        id="health_check_job",
        replace_existing=True
    )

    # 启动
    scheduler.start()
    print("定时健康检查任务已启动")