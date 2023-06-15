#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：models.py
@Author  ：xionzhi
@Date    ：2023/6/13 9:28 
"""

import typing as t

from pydantic import BaseModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from apps.database import Base
from apps.schema.models import TimeStampMixin


# https://docs.sqlalchemy.org/en/20/_modules/examples/asyncio/async_orm.html


class UserOrm(Base, TimeStampMixin):
    __tablename__ = "example_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[t.Optional[str]]
    user_name: Mapped[t.Optional[str]]
    password: Mapped[t.Optional[str]]


class UserUpdate(BaseModel):
    user_name: t.Optional[str]
    email: t.Optional[str]


class UserBase(BaseModel):
    phone: str


class UserFilter(BaseModel):
    phone: t.Optional[str] = None
    keyword: t.Optional[str] = None
    page: t.Optional[int] = 1
    size: t.Optional[int] = 10


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    user_name: t.Optional[str]
    email: t.Optional[str]

    class Config:
        orm_mode = True
