#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：test_user_service.py
@Author  ：xionzhi
@Date    ：2023/6/15 11:47 
"""

import pytest
from httpx import AsyncClient

from apps.routers.user import models


@pytest.mark.anyio
async def test_docs(app, client: AsyncClient):
    response = await client.get("/docs")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_user(client: AsyncClient, user):
    response = await client.get(f"/v1/api/user/{user.id}")

    assert response.status_code == 200
    t_user = models.User(**response.json())
    assert t_user.phone == user.phone


@pytest.mark.anyio
async def test_create_user(client: AsyncClient, user):
    pass


@pytest.mark.anyio
async def test_update_user(client: AsyncClient, user):
    pass


@pytest.mark.anyio
async def test_delete_user(client: AsyncClient, user):
    pass


@pytest.mark.anyio
async def test_list_user(client: AsyncClient, user):
    response = await client.get(f"/v1/api/user", params={'keyword': 'haha'})

    assert response.status_code == 200
    assert isinstance(response.json(), list) is True
