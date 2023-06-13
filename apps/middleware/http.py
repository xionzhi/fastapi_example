#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：http.py
@Author  ：xionzhi
@Date    ：2023/6/13 10:28 
"""

import asyncio
import time
import traceback
import typing as t

from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.responses import Response

from apps.schema.response import InternalErrorResponse
from apps.util.log import logger


async def http_middleware(request: Request, call_next: t.Callable) -> Response:
    """
    http请求接收/返回中间件
    捕获接口异常处理
    :param request:
    :param call_next:
    :return:
    """
    try:
        if asyncio.iscoroutinefunction(call_next):
            response = await call_next(request)
        else:
            response = call_next(request)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
        model = InternalErrorResponse()
        response = ORJSONResponse(
            content=model.dict(),
            status_code=model.code
        )
    finally:
        pass
    return response


async def http_process_time(request: Request, call_next: t.Callable) -> Response:
    """
    http请求接收/返回中间件
    添加response headers：接口处理时间
    :param request:
    :param call_next:
    :return:
    """
    start_time = time.perf_counter()
    if asyncio.iscoroutinefunction(call_next):
        response = await call_next(request)
    else:
        response = call_next(request)
    process_time = round((time.perf_counter() - start_time) * 1000, 3)
    response.headers['X-Process-Time'] = str(process_time)
    logger.info(f'{request.headers.get("X-Request-ID".lower(), "")}|{request.client.host}|{request.method}|'
                f'{request.url.path}|process: {process_time}ms\n')
    return response
