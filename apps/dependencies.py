#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：dependencies.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:29 
"""

import typing as t

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from apps.util.connect import AsyncRedis


def get_db(request: Request):
    return request.app.state.mysql


def get_redis(request: Request):
    return request.app.state.redis


def get_mongo(request: Request):
    return request.app.state.mongo


DbSession = t.Annotated[AsyncSession, Depends(get_db)]

RedisStore = t.Annotated[AsyncRedis, Depends(get_redis)]

DbMongo = t.Annotated[AsyncIOMotorClient, Depends(get_mongo)]
