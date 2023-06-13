#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：connect.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:48 
"""

import aioredis as aioredis
import redis as redis
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from requests import adapters, Session
from sqlalchemy import create_engine, Engine, make_url
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from urllib3 import Retry


def sync_engine(url, **kwargs) -> Engine:
    url = make_url(url)
    engine = create_engine(url, **kwargs)
    return engine


def async_engine(url, **kwargs) -> AsyncEngine:
    url = make_url(url)
    engine = create_async_engine(url, **kwargs)
    return engine


class SyncRedis:
    __slots__ = (
        "url",
        "client"
    )
    manager = dict()

    def __init__(self, url, **kwargs):
        self.url = url
        self.client = self.init_connect(url, **kwargs)

    @property
    def peer_name(self) -> str:
        return self.url

    @staticmethod
    def _make_client(url, **kwargs) -> redis.Redis:
        client = redis.Redis.from_url(
            url=url,
            **kwargs
        )
        return client

    def init_connect(self, url, **kwargs):
        if self.manager.get(self.peer_name):
            self.client = self.manager[self.peer_name]
            return self.client
        self.client = self._make_client(url, **kwargs)
        self.manager[self.peer_name] = self.client
        return self.client


class AsyncRedis:
    __slots__ = (
        "url",
        "client"
    )
    manager = dict()

    def __init__(self, url, **kwargs):
        self.url = url
        self.client = self.init_connect(url, **kwargs)

    @property
    def peer_name(self) -> str:
        return self.url

    @staticmethod
    def _make_client(url, **kwargs) -> aioredis.Redis:
        client = aioredis.from_url(
            url=url,
            **kwargs
        )
        return client

    def init_connect(self, url, **kwargs):
        if self.manager.get(self.peer_name):
            self.client = self.manager[self.peer_name]
            return self.client
        self.client = self._make_client(url, **kwargs)
        self.manager[self.peer_name] = self.client
        return self.client


class RequestsSession(Session):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
            return cls._instance
        return cls._instance

    def __init__(self, time_out=30, pool_num=10, pool_max_size=50):
        super().__init__()
        self._time_out = time_out
        self._pool_num = pool_num
        self._pool_max_size = pool_max_size
        retry = Retry(connect=3, backoff_factor=0.5)

        self.mount("api://", adapters.HTTPAdapter(
            pool_connections=self._pool_num,
            pool_maxsize=self._pool_max_size,
            max_retries=retry
        ))
        self.mount("https://", adapters.HTTPAdapter(
            pool_connections=self._pool_num,
            pool_maxsize=self._pool_max_size,
            max_retries=retry
        ))


class AsyncClientSession:
    """
    async aiohttp client
    """
    __slots__ = (
        "session",
    )

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance'):
            cls._instance = super(AsyncClientSession, cls).__new__(cls)
            return cls._instance
        return cls._instance

    def __init__(self):
        self.session = None

    async def init_session(self) -> ClientSession:
        tcp_connector = TCPConnector(
            keepalive_timeout=50,
            limit=100,
            limit_per_host=50,
        )
        self.session = ClientSession(
            connector=tcp_connector,
            timeout=ClientTimeout(total=300)
        )
        return self.session

    async def close(self):
        await self.session.close()
