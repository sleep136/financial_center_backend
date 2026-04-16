from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.health_checker import run_all_health_checks
from config.settings import settings
from filelock import FileLock
import os
import asyncio

# 全局唯一调度器
scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")

# 锁文件路径（确保多进程只有一个能启动调度器）
LOCK_FILE = "scheduler.lock"
lock = FileLock(LOCK_FILE, timeout=1)

def start_scheduler():
    """
    带文件锁的安全启动：
    解决 uvicorn 多 worker 导致的定时任务重复执行问题
    """
    try:
        # 尝试获取锁，只有第一个进程能拿到
        lock.acquire()
        print("✅ 成功获取锁，准备启动健康检查调度器")

        if scheduler.running:
            print("ℹ️ 调度器已在运行，跳过启动")
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
        print("✅ 定时健康检查任务已启动")

    except TimeoutError:
        # 其他进程拿不到锁，不启动
        print("ℹ️ 其他进程已启动调度器，当前进程跳过启动")
    finally:
        # 释放锁（不影响已启动的调度器）
        try:
            lock.release()
        except:
            pass