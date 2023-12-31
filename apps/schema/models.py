#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：models.py
@Author  ：xionzhi
@Date    ：2023/6/13 15:01 
"""
from datetime import datetime

from sqlalchemy import event, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column()
    created_at._creation_order = 9998
    updated_at: Mapped[datetime] = mapped_column()
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @staticmethod
    def _created_at(mapper, connection, target):
        _utcnow = datetime.utcnow()
        target.created_at, target.updated_at = _utcnow, _utcnow

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_insert", cls._created_at)
        event.listen(cls, "before_update", cls._updated_at)
