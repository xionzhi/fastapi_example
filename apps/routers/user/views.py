#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：views.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:28 
"""

import typing as t
from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from ..user import service, models
from ...dependencies import DbSession, RedisStore
from ...exceptions import InvalidConfigurationError
from ...schema.response import SuccessResponse, InternalErrorResponse
from ...util.log import logger

router = APIRouter()


@router.get("/{user_id}", response_model=models.User)
async def read_user(db_session: DbSession, user_id: int):
    user = await service.get_user(db_session=db_session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=models.User)
async def create_user(redis_store: RedisStore, db_session: DbSession, user_in: models.UserCreate):
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


@router.put("/{user_id}", response_model=models.User)
async def update_user(db_session: DbSession, user_id: int, user_in: models.UserUpdate):
    user = await service.get_user(db_session=db_session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = await service.update_user(db_session=db_session, user=user, user_in=user_in)
    return user


@router.delete("/{user_id}")
async def update_user(db_session: DbSession, user_id: int):
    ok, msg = await service.delete_user(db_session=db_session, user_id=user_id)
    model = SuccessResponse() if ok else InternalErrorResponse()

    return ORJSONResponse(
        content=model.dict(),
        status_code=model.code
    )


@router.get("", response_model=t.List[models.User])
async def list_user(db_session: DbSession, keyword: t.Union[str, None] = None):
    users = await service.get_all_user(db_session=db_session, keyword=keyword)

    return users
