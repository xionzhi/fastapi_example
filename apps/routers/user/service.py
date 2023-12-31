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
from sqlalchemy.ext.asyncio import AsyncSession

from apps.routers.user.models import UserOrm, UserCreate, UserUpdate
from apps.util.log import logger


async def get_user(*, db_session: AsyncSession, user_id: int) -> t.Optional[UserOrm]:
    query = (select(UserOrm).filter(UserOrm.id == user_id))
    result = await db_session.scalars(query)
    user = result.one()

    return user


async def create_user(*, db_session: AsyncSession, user_in: UserCreate) -> t.Optional[UserOrm]:
    user = UserOrm(
        **user_in.dict(exclude={"password"})
    )
    user.password = user.hash_password(user_in.password)
    db_session.add(user)
    await db_session.commit()

    return user


async def update_user(*, db_session: AsyncSession, user: UserOrm, user_in: UserUpdate) -> t.Optional[UserOrm]:
    user_data, update_data = user.dict(), user_in.dict()
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    await db_session.commit()

    return user


async def create_or_update_user(*, db_session: AsyncSession, user_in: UserUpdate) -> t.Optional[UserOrm]:
    pass


async def delete_user(*, db_session: AsyncSession, user_id: int) -> t.Tuple[bool, str]:
    if user_id == 1:
        return True, ''
    return False, 'error message'


async def get_user_by_phone(*, db_session: AsyncSession, phone: str) -> t.Optional[UserOrm]:
    query = (select(UserOrm).filter(UserOrm.phone == phone))
    result = await db_session.scalars(query)
    user = result.first()

    return user


async def get_all_user(*, db_session: AsyncSession,
                       keyword: str, phone: str, page: int, size: int, **kwargs) -> t.Sequence[t.Optional[UserOrm]]:
    """query user list"""
    query = select(UserOrm)
    if phone:
        query = query.filter(UserOrm.phone == phone)

    if keyword:
        query = query.filter(UserOrm.user_name.like(f'%{keyword}%'))

    if page and size:
        query = query.limit(size).offset((page - 1) * size)

    logger.info(f'{query.params()}')
    result = await db_session.scalars(query)
    users = result.all()

    return users


async def test_redis(*, redis_store, user_id: int) -> bool:
    return await redis_store.set(f'hello:{user_id}', 1)
