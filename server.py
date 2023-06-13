#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：server.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:24 
"""

import uvicorn
from uvicorn.loops import auto

from apps import config


def run():
    auto.auto_loop_setup()
    uvicorn.run(
        app='apps.main:get_app',
        host=config.SERVE_HOST,
        port=config.SERVE_PORT,
        workers=config.SERVE_WORKERS,
        access_log=False
    )


if __name__ == '__main__':
    run()
