# -*- encoding: utf-8 -*-
"""
@File    :   operator.py    
@Contact :   puyongjun@flashhold.com
@License :   (C)Copyright 2021-2025

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/3/19 11:43   parker      1.0         None
"""


def median(data: list):
    """
    计算中位数
    :param data:
    :return:
    """
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2
