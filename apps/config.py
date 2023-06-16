#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：__init__.py.py
@Author  ：xionzhi
@Date    ：2023/6/13 10:04 
"""

from urllib import parse

from pydantic import BaseModel
from starlette.config import Config
from starlette.datastructures import Secret

from apps.util.log import logger


class BaseConfigurationModel(BaseModel):
    """Base configuration model used by all config options."""
    pass


config = Config(".env")
logger.info(f'Config: \n{config.file_values}')

# log
LOG_LEVEL = config("LOG_LEVEL")
ENV = config("ENV", default="local")

# host
SERVE_HOST = config("SERVE_HOST", default="localhost")
SERVE_PORT = config("SERVE_PORT", default=8000)
SERVE_WORKERS = config("SERVE_WORKERS", default=1)
ENCRYPTION_KEY = config("EXAMPLE_ENCRYPTION_KEY", default=None, cast=Secret)

# jwt
JWT_AUDIENCE = config("DISPATCH_JWT_AUDIENCE", default=None)
JWT_EMAIL_OVERRIDE = config("DISPATCH_JWT_EMAIL_OVERRIDE", default=None)
JWT_SECRET = config("DISPATCH_JWT_SECRET", default=None)
JWT_ALG = config("DISPATCH_JWT_ALG", default="HS256")
JWT_EXP = config("DISPATCH_JWT_EXP", cast=int, default=86400)  # Seconds

# database
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME", default="127.0.0.1")
DATABASE_CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret)
# this will support special chars for credentials
_DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
_QUOTED_DATABASE_PASSWORD = parse.quote(str(_DATABASE_CREDENTIAL_PASSWORD))
# def
DATABASE_USER = config("DATABASE_USER", default="root")
DATABASE_PASSWD = config("DATABASE_PASSWD", default="123456")
DATABASE_NAME = config("DATABASE_NAME", default="example")
DATABASE_PORT = config("DATABASE_PORT", default="3306")
DATABASE_ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
DATABASE_ENGINE_MAX_OVERFLOW = config("DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=0)
SQLALCHEMY_DATABASE_URI = f"mysql+aiomysql://" \
                          f"{DATABASE_USER}:{DATABASE_PASSWD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
SYNC_SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://" \
                               f"{DATABASE_USER}:{DATABASE_PASSWD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

# redis
REDIS_STORE_HOST = config("REDIS_STORE_HOST", default="127.0.0.1")
REDIS_STORE_PORT = config("REDIS_STORE_PORT", default="6379")
REDIS_STORE_URI = f"redis://{REDIS_STORE_HOST}:{REDIS_STORE_PORT}"


MONGO_CONFIG = {
    'HOST': config("MONGO_HOST", default="127.0.0.1"),
    'PORT': config("MONGO_PORT", default="27017"),
    'USER': config("MONGO_USER", default=None),
    'PASSWORD': config("MONGO_PASSWORD", default=None),
    'AUTH_DB': config("MONGO_AUTH_DB", default=None),
}
