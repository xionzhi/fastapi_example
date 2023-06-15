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

from apps.routers.user.models import UserOrm, UserCreate, UserUpdate
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
            await session.commit()
    return user


async def update_user(*, db_session, user_id: int, user_in: UserUpdate) -> t.Optional[UserOrm]:
    async with db_session() as session:
        async with session.begin():
            query = (select(UserOrm).filter(UserOrm.id == user_id))
            user = (await session.scalars(query)).one()

            user_data, update_data = user.dict(), user_in.dict()
            for field in user_data:
                if field in update_data:
                    setattr(user, field, update_data[field])

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


async def get_all_user(*, db_session,
                       keyword: str, phone: str, page: int, size: int, **kwargs) -> t.List[t.Optional[UserOrm]]:
    async with db_session() as session:
        query = select(UserOrm)

        if phone:
            query = query.filter(UserOrm.phone == phone)

        if keyword:
            query = query.filter(UserOrm.user_name.like(f'%{keyword}%'))

        if page and size:
            query = query.limit(size).offset((page - 1) * size)

        logger.info(f'{query.params()}')
        result = await session.scalars(query)
        users = result.all()
    return users


async def test_redis(*, redis_store, user_id: int) -> bool:
    return await redis_store.set(f'hello:{user_id}', 1)
