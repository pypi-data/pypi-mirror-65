#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepTricks.
# @File         : __init__.py
# @Time         : 2019-09-10 14:48
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import os
import numpy as np

from .cprint import cprint
from .timer import timer
from .logger import *
from .pipe import *

get_module_path = lambda path, file=__file__: \
    os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))


def noramlize(x):
    return x / np.linalg.norm(x, 2, axis=len(x.shape) > 1, keepdims=True)
