# -*- coding: utf-8 -*-
"""

这里检查对象 属性 是否满足 某些条件,进行 特定返回值 .

"""

import functools
import inspect


def checked_arguments(f):
    @functools.wraps(f)
    def wrapper(*a, **k):
        sig = inspect.signature(f).bind(*a, **k)
        sig.apply_defaults()
        d = sig.arguments

        valid_val = check_arguments(d)
        if valid_val:
            return f(*a, **k)
        else:
            return {
                'score': 0,
                'prob': 0
            }

    return wrapper


def check_arguments(d):
    """
    这里是 检查 参数的条件, 这里可以随便写 .
    :param d:
    :return:
    """
    args = d.get('args')
    kw = d.get('kwargs')

    # 这里检查 只要参数存在 就进行计算,否则 不计算
    if not any(args):
        if not any(kw.values()):
            return False

    return True


@checked_arguments
def run(*args, **kwargs):
    """
    模型函数,计算分值用的.
    :param args:
    :param kwargs:
    :return:
    """
    return (args, kwargs)


if __name__ == '__main__':
    print(run(a=1))  # ((), {'a': 1})
    print(run())  # {'score': 0, 'prob': 0}
