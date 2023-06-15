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
from sqlalchemy import Table

from apps import config
from apps.util.connect import async_engine, sync_engine


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


class Base(AsyncAttrs, DeclarativeBase):

    @classmethod
    def __table_cls__(cls, name, metadata_obj, *arg, **kw):
        return Table(name, metadata_obj, *arg, **kw)
        # return Table(f"example_{name}", metadata_obj, *arg, **kw)

    def dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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
