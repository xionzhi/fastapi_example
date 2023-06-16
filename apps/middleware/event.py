#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：event.py
@Author  ：xionzhi
@Date    ：2023/6/13 10:28 
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from starlette.requests import Request
from starlette.routing import Route

from apps import config
from apps.database import async_msql_engine
from apps.schema.response import RequestValidErrorResponse
from apps.util.connect import AsyncClientSession, AsyncRedis, AsyncMongodb
from apps.util.log import logger


def register_app_middleware(app: FastAPI):
    @app.on_event('startup')
    async def startup_event():
        app.state.config = config
        app.state.redis = AsyncRedis(url=config.REDIS_STORE_URI, decode_responses=True).client
        app.state.client = await AsyncClientSession().init_session()
        app.state.mysql = async_sessionmaker(async_msql_engine, class_=AsyncSession, expire_on_commit=False)
        app.state.mongo = AsyncMongodb(config.MONGO_CONFIG).client

        route: Route
        for route in app.routes:
            logger.debug(f'{route.methods} {route.path}')

    @app.on_event('shutdown')
    async def shutdown_event():
        await app.state.redis.close()
        await app.state.client.close()

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
            request: Request,
            exc: RequestValidationError
    ):
        model = RequestValidErrorResponse(data=exc.errors())
        response = ORJSONResponse(
            content=model.dict(),
            status_code=model.code
        )
        return response

    return app
