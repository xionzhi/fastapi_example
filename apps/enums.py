#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fastapi_example 
@File    ：enums.py
@Author  ：xionzhi
@Date    ：2023/6/13 15:55 
"""

from enum import Enum


class ExampleEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)
