#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：service.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:29 
"""

import typing as t

from sqlalchemy import select, update

from apps.routers.user.models import UserOrm, UserCreate, UserUpdate, UserFilter
from apps.util.log import logger


async def get_user(*, db_session, user_id: int) -> t.Optional[UserOrm]:
    async with db_session() as session:
        query = (select(UserOrm).filter(UserOrm.id == user_id))
        result = await session.scalars(query)
        user = result.one()
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


async def update_user(*, db_session, user: UserOrm, user_in: UserUpdate) -> t.Optional[UserOrm]:
    user_data, update_data = user.dict(), user_in.dict(skip_defaults=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    async with db_session() as session:
        async with session.begin():
            query = (update(UserOrm).
                     filter(UserOrm.id == user.id).
                     values(**user_in.dict()))
            await session.execute(query)
            await session.commit()
    return user


async def create_or_update_user(*, db_session, user_in: UserUpdate) -> t.Optional[UserOrm]:
    pass


async def delete_user(*, db_session, user_id: int) -> t.Tuple[bool, str]:
    if user_id == 1:
        return True, ''
    return False, 'error message'


async def get_user_by_phone(*, db_session, phone: str) -> t.Optional[UserOrm]:
    async with db_session() as session:
        query = (select(UserOrm).filter(UserOrm.phone == phone))
        result = await session.scalars(query)
        user = result.first()
    return user


async def get_all_user(*, db_session, keyword: str) -> t.List[t.Optional[UserOrm]]:
    async with db_session() as session:
        query = select(UserOrm)

        if keyword:
            query = query.filter(UserOrm.user_name.like(f'%{keyword}%'))

        result = await session.scalars(query)
        users = result.all()
    return users


async def test_redis(*, redis_store, user_id: int) -> bool:
    return await redis_store.set(f'hello:{user_id}', 1)
