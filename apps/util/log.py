#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：log.py
@Author  ：xionzhi
@Date    ：2023/6/13 10:36 
"""

import os
from pathlib import Path

from loguru import logger as _logger

__base_path = Path(__file__).parent.parent
__base_log_path = os.path.join(__base_path, "log")
__api_log_path = os.path.join(__base_log_path, "api")
__api_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {thread.name} | {name} | {function} | {line} | {message}"
__api_handles = [
    {
        "sink": "%s/{time:YYYYMMDD}.log" % __api_log_path,
        "enqueue": True,
        "backtrace": True,
        "rotation": "00:00",
        "retention": "3 days",
        "format": __api_format,
        "filter": lambda x: x["extra"].get("channel", '') == "api"
    }
]
__celery_log_path = os.path.join(__base_log_path, "celery")
__celery_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {process.name} | {name} | {function} | {line} | {message}"
__celery_handles = [
    {
        "sink": "%s/{time:YYYYMMDD}.log" % __celery_log_path,
        "enqueue": True,
        "backtrace": True,
        "rotation": "00:00",
        "retention": "3 days",
        "format": __celery_format,
        "filter": lambda x: x["extra"].get("channel", '') == "celery"
    }
]

_channel = {
    'api': __api_handles,
    'celery': __celery_handles,
}


class UdfLogger:
    __conn = {}

    def __init__(self, channel: str):
        if not self.__conn.get(channel):
            self.channel = channel
            handlers = _channel.get(channel, 'api')
            assert handlers is not None, 'channel not match handlers'
            _ = [_logger.add(**h) for h in handlers]
            client = _logger.bind(channel=channel)
            self.__conn.setdefault(channel, client)
        self.client = self.__conn[channel]


logger = UdfLogger('api').client
celery_logger = UdfLogger('celery').client
