from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.health_checker import run_all_health_checks
from config.settings import settings
from filelock import FileLock
import atexit

# --------------------------
# 全局锁：整个进程唯一抢占
# --------------------------
LOCK_PATH = "scheduler.lock"
lock = FileLock(LOCK_PATH, timeout=2)

# 只有抢占到锁的进程才会创建调度器
# 没抢到的 = 调度器永远为空
scheduler = None

try:
    # 抢占锁，只有1个worker能成功
    lock.acquire()
    print("✅ [Scheduler] 本worker抢占成功，启动定时任务")

    # 只有抢到锁的进程才初始化调度器
    scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")

except TimeoutError:
    # 其他3个worker直接跳过
    print("ℹ️ [Scheduler] 其他worker已抢占锁，本worker不启动")


def start_scheduler():
    """只有抢到锁的worker才会真正启动任务"""
    global scheduler

    # 没抢到锁的进程直接跳过，绝不启动
    if scheduler is None:
        return

    if scheduler.running:
        return

    # 只添加一次
    scheduler.add_job(
        run_all_health_checks,
        trigger="interval",
        seconds=settings.CHECK_INTERVAL,
        id="health_check_job",
        replace_existing=True
    )

    scheduler.start()
    print("✅ [Scheduler] 健康检查定时任务已启动")


# 程序退出时自动释放锁
def release_lock():
    try:
        lock.release()
    except:
        pass


atexit.register(release_lock)