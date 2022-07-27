# -*- encoding: utf-8 -*-
"""
@File    :   str.py    
@Contact :   puyongjun@flashhold.com
@License :   (C)Copyright 2021-2025

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/5 13:28   parker      1.0         None
"""
import hashlib
import re
import datetime


def gen_md5(value):
    """
    根据输入值编码为 md5
    :param value: 输入值
    :return:
    """
    return hashlib.md5(value.encode(encoding='UTF-8')).hexdigest()


def str_is_compile(value, compile_str) -> bool:
    """
    匹配一个字符串是否包含某个正则
    :param value:
    :param compile_str:
    :return:
    """
    r = []
    try:
        r = re.findall(compile_str, value)
    except Exception as e:
        print(e)
    return True if len(r) >= 1 else False


def str_to_time(st: str, _format="%Y-%m-%d %H:%M:%S", _default=None):
    """
    字符串格式化为时间
    :param st:
    :param _format:
    :param _default:
    :return:
    """
    try:
        return datetime.datetime.strptime(st, _format)
    except Exception as e:
        if _default:
            return _default
        raise e


def str_is_none(st: str) -> bool:
    """
    判断字符串是否为null
    :param st:
    :return:
    """
    _null_arr = ["NULL", "NONE"]
    if not st or not str(st).strip() or str(st).upper().strip() in _null_arr:
        return True
    return False


def str_default(st: str, _default=-9999999):
    if str_is_none(st):
        return _default
    return st
