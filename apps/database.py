#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：database.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:29 
"""

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from apps import config
from apps.util.connect import async_engine, sync_engine


class Base(AsyncAttrs, DeclarativeBase):
    pass


sync_mysql_engine = sync_engine(
    url=config.SYNC_SQLALCHEMY_DATABASE_URI,
    pool_size=config.DATABASE_ENGINE_POOL_SIZE,
    max_overflow=config.DATABASE_ENGINE_MAX_OVERFLOW,
)

async_msql_engine = async_engine(
    url=config.SQLALCHEMY_DATABASE_URI,
    pool_size=config.DATABASE_ENGINE_POOL_SIZE,
    max_overflow=config.DATABASE_ENGINE_MAX_OVERFLOW,
)
