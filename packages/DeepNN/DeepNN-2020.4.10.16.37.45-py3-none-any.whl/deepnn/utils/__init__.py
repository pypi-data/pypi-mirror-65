#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepTricks.
# @File         : __init__.py
# @Time         : 2019-09-10 14:48
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import numpy as np
from functools import *
from pathlib import Path

from .cprint import cprint
from .timer import timer
from .logger import *




class pipe:
    """I am very like a linux pipe"""

    def __init__(self, function):
        self.function = function
        update_wrapper(self, function)

    def __ror__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return pipe(lambda x: self.function(x, *args, **kwargs))


def noramlize(x):
    return x / np.linalg.norm(x, 2, axis=len(x.shape) > 1, keepdims=True)
