# -*- encoding: utf-8 -*-
"""
@File    :   arr.py
@Contact :   puyongjun@flashhold.com
@License :   (C)Copyright 2021-2025

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/5 10:07   parker      1.0         针对数组的处理
"""


def get_arr_data(arr, n, default=None):
    """
    这个函数的作用是获取数组中的某个位置的值
    :param arr:数组
    :param n:数组中的位置
    :param default:默认值
    :return:存在则返回相关的值，不存在则返回 None
    """
    if len(arr) <= n:
        return default
    return arr[n]
