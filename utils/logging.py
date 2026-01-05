from flask import request
import logging
import logging.handlers
import os

from config.settings import settings


class RequestFormatter(logging.Formatter):
    """
    针对请求信息的日志格式
    """

    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


def create_logger():
    """
    设置日志
    :param app: app对象
    :return:
    """
    logging_file_dir = './logs'
    logging_file_max_bytes = 300 * 1024 * 1024
    logging_file_backup = 10
    logging_level = "DEBUG"

    fastapi_console_handler = logging.StreamHandler()
    fastapi_console_handler.setFormatter(logging.Formatter('%(levelname)s %(module)s %(lineno)d %(message)s'))

    request_formatter = RequestFormatter('%(levelname)s [%(asctime)s] %(remote_addr)s -> %(url)s '
                                         '%(module)s %(lineno)d: %(message)s')

    fastapi_file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(logging_file_dir, 'financial_center_backend.log'),
        mode="a",
        maxBytes=logging_file_max_bytes,
        backupCount=logging_file_backup
    )
    fastapi_file_handler.setFormatter(request_formatter)

    log_fastapi_app = logging.getLogger('financial_center_backend.app')
    log_fastapi_app.addHandler(fastapi_file_handler)
    log_fastapi_app.setLevel(logging_level)

    log_fastapi_app.addHandler(log_fastapi_app)
