# -*- coding: utf-8 -*- 

import typing
from functools import wraps


def element_mapping(factor_name):
    """ 用来 修饰 类方法的返回结果,如果 返回为不是一个字典类型, 转成字典返回  {factor_name:value},
        如果返回 类型 是一个字典类型 , 则直接返回, 不做任何处理.

    :param factor_name: str  因子名称
    :return: dict

    """

    def decoration(fn):
        @wraps(fn)
        def wrapper(cls, *args, **kwargs):
            value = fn(cls, *args, **kwargs)
            if value is None:
                return {}
            if isinstance(value, typing.Mapping):
                return value
            return {factor_name: value}

        return wrapper

    return decoration


class Person:

    @element_mapping(factor_name='person')
    def calcalute(self):
        return 10

    @classmethod
    @element_mapping(factor_name='pick')
    def pickup(cls):
        return 20


if __name__ == '__main__':
    p = Person()

    print(p.calcalute())
    print(p.pickup())
    pass
