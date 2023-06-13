#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：server.py
@Author  ：xionzhi
@Date    ：2023/6/13 15:51 
"""

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from apps.middleware.event import register_app_middleware
from apps.middleware.http import http_middleware, http_process_time
from apps.routers.user.views import router as user_router


api_router = APIRouter(
    default_response_class=ORJSONResponse
)


api_router.include_router(
    user_router, prefix="/user", tags=["user"]
)


def get_app():
    app = FastAPI(
        title='FastapiExample',
        description='FastapiExample',
        version='0.0.1',
        default_response_class=ORJSONResponse,
    )
    # 注册中间件
    register_app_middleware(app)
    app.middleware('http')(http_middleware)
    app.middleware('http')(http_process_time)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # 注册路由
    app.include_router(
        router=api_router,
        prefix='/v1/api'
    )
    return app


# gunicorn "main:get_app" --worker-class uvicorn.workers.UvicornWorker
