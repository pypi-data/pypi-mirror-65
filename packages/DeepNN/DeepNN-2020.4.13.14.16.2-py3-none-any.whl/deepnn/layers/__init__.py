#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepTricks.
# @File         : __init__.py
# @Time         : 2019-09-10 15:22
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import tensorflow as tf

from .Add import Add
from .NoMask import NoMask
from .Linear import Linear
from tensorflow.keras.layers import Dense

from tensorflow.keras.models import *
from tensorflow.keras.layers import *
Dense

def add_func(inputs):
    return Add()(inputs)


def concat_func(inputs, axis=-1, mask=False):
    if not mask:
        inputs = list(map(NoMask(), inputs))
    if len(inputs) == 1:
        return inputs[0]
    else:
        return tf.keras.layers.Concatenate(axis=axis)(inputs)

# from functools import partial
# from collections import Iterable
#
# from keras.layers import Dense
#
# # last layer: 'softmax' or 'sigmoid'
# def getDenseList(unitsList, activation=None):
#     assert isinstance(unitsList, Iterable)
#     dense = partial(Dense, activation=activation)
#     return map(dense, unitsList)
