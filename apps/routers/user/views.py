#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：views.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:28 
"""

from fastapi import APIRouter, HTTPException
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from ..user import service, models
from ...dependencies import DbSession, RedisStore
from ...exceptions import InvalidConfigurationError
from ...util.log import logger

router = APIRouter()


@router.get("/{user_id}", response_model=models.User)
async def read_user(user_id: int, db_session: DbSession):
    user = await service.get_user(db_session=db_session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=models.User)
async def read_user(user_in: models.UserCreate, redis_store: RedisStore, db_session: DbSession):
    user = await service.get_user_by_phone(db_session=db_session, phone=user_in.phone)
    if user:
        raise ValidationError(
            [
                ErrorWrapper(
                    InvalidConfigurationError(msg="A user with this phone already exists."),
                    loc="phone",
                )
            ],
            model=models.UserCreate,
        )

    user = await service.create_user(db_session=db_session, user_in=user_in)

    redis_status = await service.test_redis(redis_store=redis_store, user_id=user.id)
    logger.info(redis_status)

    return user
