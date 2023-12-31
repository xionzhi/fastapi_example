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
from ...dependencies import DbSession, RedisStore, DbMongo
from ...exceptions import InvalidConfigurationError
from ...schema.response import SuccessResponse, ExternalInvokeErrorResponse
from ...util.log import logger

router = APIRouter()


@router.get("/test_mongo", response_model=t.Dict)
async def test_mongo(redis_store: RedisStore, db_mongo: DbMongo):
    doc = await db_mongo.test['crawlSeedV3'].find_one({}, {'_id': 0})

    # test redis
    redis_status = await service.test_redis(redis_store=redis_store, user_id=1)
    logger.info(f'test_redis: {redis_status}')

    return doc


@router.get("/test_mongo_list", response_model=t.List[t.Dict])
async def test_mongo(db_mongo: DbMongo):
    docs = [doc async for doc in
            db_mongo.webpage['amazon_tmp_webpage110']
            .find({'htmlIntegrity': 'OK'},
                  {'_id': 0, 'metadata': 0, 'signature': 0, 'content': 0, 'prevSignature': 0}).limit(10)]
    return docs


@router.get("/{user_id}", response_model=models.User)
async def read_user(db_session: DbSession, user_id: int):
    user = await service.get_user(db_session=db_session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=models.User)
async def create_user(db_session: DbSession, user_in: models.UserCreate):
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

    # test check passwd
    check = user.check_password(user_in.password)
    logger.info(f'check_password: {check}')

    return user


@router.put("/{user_id}", response_model=models.User)
async def update_user(db_session: DbSession, user_id: int, user_in: models.UserUpdate):
    user = await service.get_user(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = await service.update_user(db_session=db_session, user=user, user_in=user_in)
    return user


@router.delete("/{user_id}")
async def delete_user(db_session: DbSession, user_id: int):
    ok, msg = await service.delete_user(db_session=db_session, user_id=user_id)
    model = SuccessResponse() if ok else ExternalInvokeErrorResponse(message=msg)

    return ORJSONResponse(
        content=model.dict(),
        status_code=model.code
    )


@router.get("", response_model=t.List[models.User])
async def list_user(db_session: DbSession,
                    phone: t.Optional[str] = None,
                    keyword: t.Optional[str] = None,
                    page: t.Optional[int] = 1,
                    size: t.Optional[int] = 10):
    user_filter = models.UserFilter(phone=phone, keyword=keyword, page=page, size=size)
    users = await service.get_all_user(db_session=db_session, **user_filter.dict())

    return users
