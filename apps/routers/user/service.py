#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：service.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:29 
"""

import typing as t

from sqlalchemy import select

from apps.routers.user.models import UserOrm, User, UserCreate


async def get_user(*, db_session, user_id: int) -> t.Optional[User]:
    async with db_session() as session:
        # print(type(session))  # <class 'sqlalchemy.ext.asyncio.session.AsyncSession'>
        # from sqlalchemy.ext.asyncio.session import AsyncSession
        query = (select(UserOrm).filter(UserOrm.id == user_id))
        result = await session.scalars(query)
        user = result.first()
    return user


async def create_user(*, db_session, user_in: UserCreate) -> t.Optional[UserOrm]:
    user = UserOrm(
        **user_in.dict(exclude={"password"}), password=user_in.password
    )

    async with db_session() as session:
        async with session.begin():
            session.add(user)
            # await session.flush()
            await session.commit()
    return user


async def get_user_by_phone(*, db_session, phone: str) -> t.Optional[User]:
    async with db_session() as session:
        query = (select(UserOrm).filter(UserOrm.phone == phone))
        result = await session.scalars(query)
        user = result.first()
    return user


async def test_redis(*, redis_store, user_id: int) -> bool:
    return await redis_store.set(f'hello:{user_id}', 1)
