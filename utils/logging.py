from fastapi import Request
import logging
import logging.handlers
import os
from typing import Optional

from config.settings import settings


class RequestFormatter(logging.Formatter):
    """
    针对请求信息的日志格式
    """

    def format(self, record):
        # 从记录中获取请求对象
        request: Optional[Request] = getattr(record, 'request', None)
        if request:
            record.url = str(request.url) if request.url else ""
            record.remote_addr = request.client.host if request.client else ""
        else:
            record.url = ""
            record.remote_addr = ""
        return super().format(record)


def create_logger():
    """
    设置日志
    :return: 配置好的logger对象
    """
    logging_file_dir = './logs'

    # 确保日志目录存在
    os.makedirs(logging_file_dir, exist_ok=True)

    logging_file_max_bytes = 300 * 1024 * 1024  # 300MB
    logging_file_backup = 10
    logging_level = "DEBUG"

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(levelname)s %(module)s %(lineno)d %(message)s')
    )

    # 创建文件处理器
    request_formatter = RequestFormatter(
        '%(levelname)s [%(asctime)s] %(remote_addr)s -> %(url)s '
        '%(module)s %(lineno)d: %(message)s'
    )

    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(logging_file_dir, 'financial_center_backend.log'),
        mode="a",
        maxBytes=logging_file_max_bytes,
        backupCount=logging_file_backup,
        encoding='utf-8'
    )
    file_handler.setFormatter(request_formatter)

    # 创建并配置logger
    logger = logging.getLogger('financial_center_backend.app')

    # 避免重复添加handler
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.setLevel(getattr(logging, logging_level))
        logger.propagate = False  # 防止日志向上传播到root logger

    return logger


# 创建全局logger实例
logger = create_logger()

# 可选：创建FastAPI中间件来注入请求信息到日志记录
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = time.time()

        # 将请求对象添加到logger的记录中
        record = logging.LogRecord(
            name='financial_center_backend.app',
            level=logging.INFO,
            pathname='',
            lineno=0,
            msg='',
            args=(),
            exc_info=None
        )
        record.request = request

        # 处理请求
        response = await call_next(request)

        # 计算处理时间
        process_time = time.time() - start_time

        # 记录请求信息
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Process time: {process_time:.3f}s",
            extra={'request': request}
        )

        return response
