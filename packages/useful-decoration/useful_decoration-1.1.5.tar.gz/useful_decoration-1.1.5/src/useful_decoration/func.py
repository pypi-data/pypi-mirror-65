# -*- coding: utf-8 -*-
"""
这里检查对象 属性 是否满足 某些条件,进行 特定返回值 .
检查 对象中 data 属性 ,是否 满足 某些条件
如果 data 满足 某些条件,可以进行计算 ; 否则不算,直接返回默认值 .

"""

import functools
from simplelog import logger

# 默认信用分
DEFAULT_SCORE = -111.0

# 默认概率分
DEFAULT_PROB = -222.0


def _check_arguments(d):
    """
    如果 d 全为空值,None ,则返回False . d.values有一个不为空,None,0 则 返回True
    """
    copy = d.copy()
    return any(copy.values())


def checked_arguments(score, prob):
    def _checked_arguments(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):

            valid_val = _check_arguments(self.data)
            if valid_val:
                return f(self, *args, **kwargs)
            else:
                logger.info(
                    f'checked_arguments failed. '
                    f'return default value: DEFAULT_SCORE:{DEFAULT_SCORE}, DEFAULT_PROB:{DEFAULT_PROB} '
                    f'class_name:{self.__class__.__name__}'
                )
                return {
                    score: DEFAULT_SCORE,
                    prob: DEFAULT_PROB
                }

        return wrapper

    return _checked_arguments


class Model:

    def __init__(self, data):
        self.data = data

    @checked_arguments(score='score', prob='prob')
    def calculate(self):
        return {
            "score": 100.0,
            "prob": 100.0,
        }


if __name__ == '__main__':
    data = {'0': None, '1': None, '6': None, '7': None, '8': None, '9': None}

    model = Model(data=data)

    r = model.calculate()

    print(f"r :{r}")
