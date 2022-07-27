# -*- encoding: utf-8 -*-
"""
@File    :   tm.py
@Contact :   puyongjun@flashhold.com
@License :   (C)Copyright 2021-2025

用来处理时间
"""
import datetime


def get_relative_now(weeks: int = 0,
                     days: int = 0,
                     hours: int = 0,
                     minutes: int = 0,
                     seconds: int = 0,
                     microseconds: int = 0,
                     milliseconds: int = 0):
    """
    获取当前时间相对时间
    """
    return datetime.datetime.now() + datetime.timedelta(
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds
    )


def get_get_relative_now_format(weeks: int = 0,
                                days: int = 0,
                                hours: int = 0,
                                minutes: int = 0,
                                seconds: int = 0,
                                microseconds: int = 0,
                                milliseconds: int = 0,
                                default: str = "%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间相对时间的格式化之后的时间
    """
    return get_relative_now(
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds
    ).strftime(default)
