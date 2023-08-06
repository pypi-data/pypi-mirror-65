# -*- coding: utf-8 -*-

import functools
import inspect
from simplelog import logger
from collections import OrderedDict

default_value = {
    'ret': 0
}


def checked_arguments(*, callback, default):
    """
    :param callback: function
            这个 callable 只接受 一个参数 Orderdict
            this  function 返回  True,or False  如果为 True 则进行 下面的逻辑 fn的逻辑,
            否则不进行 fn 的逻辑,直接返回  规定的默认值default

    :param default: 如果 不能检查 成功 ,返回 default值
    :return:
    """

    def _checked_arguments(f):
        @functools.wraps(f)
        def wrapper(*a, **k):
            sig = inspect.signature(f).bind(*a, **k)
            sig.apply_defaults()
            d = sig.arguments

            valid_val = callback(d)
            if valid_val:

                value = f(*a, **k)
                logger.info(f"return normal_value, value:{value} ")
                return value


            else:
                logger.info(f"return default_value, value:{default} ")
                return default

        return wrapper

    return _checked_arguments


def call_back(params_dict: OrderedDict):
    """
    用户自定义的一个 callback ,这个函数 返回 true or  false


    这里 自定义 a >10 我认为 检查失败
    :param params_dict:
    :return: true or false
    """
    logger.info(f"params_dict: {params_dict}")
    a = params_dict.get('a')

    if a > 10:
        return True
    return False


@checked_arguments(callback=call_back, default=default_value)
def calculate(a, b):
    """
    用户函数
    :param a:
    :param b:
    :return:
    """
    return {"ret": 20}


def case_one():
    print(calculate(2, 20))
    print(calculate(20, 20))


def case_two():
    print(predict(num=100))
    print(predict(num=1))


def predict_callback(data):
    """
    user defined
    :param data: dict
    :return:
    """

    kwargs = data.get('kwargs')
    # print(kwargs)
    num = kwargs.get('num')
    if num > 10:
        return True
    return False


@checked_arguments(callback=predict_callback, default=-100)
def predict(**kwargs):
    """
    用户函数
    :param kargs:
    :return:
    """
    return 100


def check_args(data):
    """
    这里如果判断  参数都小于10 认为可以通过检查
    :param data:
    :return:
    """

    args = data.get('args')
    max_value = max(args)

    if max_value > 10:
        return True

    return False


@checked_arguments(callback=check_args, default=-100)
def fun(*args, **kwargs):
    return 100


if __name__ == '__main__':
    fun(10, 20)
    fun(1, 2)

    pass
