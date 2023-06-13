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


class BizCode:
    SUCCESS = 0
    FAIL = 1
    DATA_NOT_FOUND = 10404
    UnknownOperate = 10400


class BaseJsonResModel(BaseModel):
    code: int = Field(title='状态码')
    message: str = Field(title='状态值说明')
    data: t.Optional[t.Union[t.Dict, str, t.List, t.Any]] = {}


class SuccessResponse(BaseJsonResModel):
    code: int = Field(default=BizCode.SUCCESS, title='状态码')
    message: str = Field(default='Success', title='状态值说明')


class FailureResponse(BaseJsonResModel):
    code: int = Field(default=BizCode.FAIL, title='状态码')
    message: str = Field(default='Failed', title='状态值说明')


class ExternalInvokeErrorResponse(FailureResponse):
    code = status.HTTP_400_BAD_REQUEST
    message = 'External Invoke Error'


class RequestValidErrorResponse(FailureResponse):
    code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = 'Request Entity Error'


class InternalErrorResponse(FailureResponse):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = 'Internal Server Error'


class NotFoundErrorResponse(BaseJsonResModel):
    code: int = Field(default=BizCode.DATA_NOT_FOUND, title='状态码')
    message: str = Field(default='Data Not Found', title='状态值说明')


class UnknownOperateErrorResponse(BaseJsonResModel):
    code: int = Field(default=BizCode.UnknownOperate, title='状态码')
    message: str = Field(default='Unknown Operate', title='状态值说明')
