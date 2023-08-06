# -*- coding: utf-8 -*-
import time
from functools import partial, wraps
from contextlib import contextmanager

from simplelog import logger

now = time.time


def fn_timer(fn=None, *, prefix="", interval=0.0):
    """
    计算 fn  的运算时间

    :param fn: 函数, callable 对象
    :param prefix: str  给函数一个标识 前缀  默认是 ""
    :param interval: float  单位是 s,  给定一个阈值,超过某一个阈值,就记录时间. 否则不记录,
                     该参数 默认值 是:0.0 ,即 记录所有的函数的运行时间.

    :return:
    """
    if fn is None:
        return partial(fn_timer, prefix=prefix, interval=interval)

    @wraps(fn)
    def function_timer(*args, **kwargs):
        start = now()
        result = fn(*args, **kwargs)
        t = now() - start
        if t >= interval:
            logger.info(f'{prefix}{fn.__name__} total running time {now() - start} seconds')
        return result

    return function_timer


@contextmanager
def code_timer(name='default'):
    """
    计算代码段的运行时间
    :param name: 用于区分不同代码段的名称
    :return:
    :usage:

     ..code-block:
         with timer('delay'):
                     time.sleep(3)
    """
    start = now()
    yield
    logger.info(f'{name} total running time {now() - start} seconds')
