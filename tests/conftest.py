#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：conftest.py
@Author  ：xionzhi
@Date    ：2023/6/14 17:53 
"""

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from apps.config import SERVE_HOST, SERVE_PORT
from apps.main import get_app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def app():
    yield get_app()


@pytest.fixture(scope="session")
async def client(app):
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url=f"http://{SERVE_HOST}:{SERVE_PORT}") as client:
            yield client


@pytest.fixture
def user():
    from apps.routers.user.models import User
    user = User(id=1, phone='13088880000')
    yield user
