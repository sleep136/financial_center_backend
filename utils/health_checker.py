import socket
import time
from redis import Redis
from config.settings import settings
from utils.logging import logger
redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)


def parse_target(target: str):
    """
    解析目标，支持：
    - domain:port
    - ip:port
    - domain（自动用 80 端口）
    """
    if "http" in target:
        host = target
        port = 80  # 无端口默认80
    else:
        host, port = target.split(":", 1)
        port = int(port)

    return host, port


def check_service_health(target: str, name) -> dict:
    host, port = parse_target(target)
    start_time = time.time()
    checked_at = time.strftime("%Y-%m-%d %H:%M:%S")

    # 1. 域名解析
    try:
        ip = socket.gethostbyname(host)
    except Exception as e:
        return {
            "healthy": 0,
            "response_time_ms": 0,
            "checked_at": checked_at,
            "resolved_ip": '',
            "resolve_error": f"域名解析失败: {str(e)}",
            "error": '',
            "name": name
        }

    # 2. TCP 连接检查
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            connect_code = s.connect_ex((ip, port))

        # 只有返回 0 才算健康
        is_healthy = 1 if (connect_code == 0) else 0
        error = f"TCP 连接失败，错误码: {connect_code}" if not is_healthy else ""

    except Exception as e:
        is_healthy = 0
        error = f"连接异常: {str(e)}"

    return {
        "healthy": is_healthy,
        "response_time_ms": round((time.time() - start_time) * 1000, 2),
        "checked_at": checked_at,
        "resolved_ip": ip,
        "error": error,
        "name": name
    }


def run_all_health_checks():
    for target,name in settings.TARGET_SERVICES.items():
        result = check_service_health(target, name)
        logger.info(f"[{result['checked_at']}] {target} → {result}")
        redis.hset(f"health:{target}", mapping=result)
