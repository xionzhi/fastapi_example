#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：response.py
@Author  ：xionzhi
@Date    ：2023/6/13 10:34 
"""

import typing as t

from pydantic import BaseModel, Field
from starlette import status


class BaseJsonResModel(BaseModel):
    code: int = Field(title='Biz Code')
    message: str = Field(title='Biz Code Message')
    data: t.Optional[t.Union[t.Dict, str, t.List, t.Any]] = {}


class SuccessResponse(BaseJsonResModel):
    code: int = Field(default=status.HTTP_200_OK, title='Biz Code')
    message: str = Field(default='Success', title='Biz Code Message')


class ExternalInvokeErrorResponse(BaseJsonResModel):
    code = status.HTTP_400_BAD_REQUEST
    message = 'External Invoke Error'


class RequestValidErrorResponse(BaseJsonResModel):
    code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = 'Request Entity Error'


class InternalErrorResponse(BaseJsonResModel):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = 'Internal Server Error'
