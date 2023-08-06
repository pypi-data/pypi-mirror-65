# -*- coding: utf-8 -*- 

"""
@Time   : 2020/4/12 19:34
@File   : single.py
@Author : 15769162764@163.com

"""
import time

from functools import update_wrapper


def single(fn):
    """
    这个函数 只会计算一次.并且对函数的参数不敏感.
    single is not  sensitive to
    argument values, and will always return the ame value if
    called with different arguments.

    :param fn:
    :return:
    """
    name = fn.__name__

    def wrapper(*args, **kw):
        if name not in single.__dict__:
            ret = fn(*args, **kw)
            single.__dict__[name] = ret
            return ret
        else:
            return single.__dict__[name]

    # copy 源数据 docstring name 等等..
    return update_wrapper(wrapper, fn)


def singleton(cls):
    """
    类装饰器 的使用,
    这样简单的可以生成一个对象
    :param cls:
    :return:
    """
    instances = dict()

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    # copy 源数据 docstring name 等等..
    return update_wrapper(wrapper, cls)


@singleton
def my_sum(a, b):
    print("my sum begin")
    # time.sleep(1)

    return a + b


@single
class Person:
    """
    This is  Person
    """
    name = "Frank"


def test_person():
    p = Person()
    p2 = Person()
    p3 = Person()

    print(p, p2, p3)

    assert p == p2 == p3

    assert id(p) == id(p2) == id(p3)


if __name__ == '__main__':
    print(my_sum(1, 4))
    print(my_sum(1, 4))
    print(my_sum(1, 4))
    print(my_sum(1, 4))

    test_person()

    pass
