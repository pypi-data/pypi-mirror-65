#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepNN.
# @File         : namedtupled_
# @Time         : 2020/4/13 11:26 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import os
import namedtupled

print(namedtupled.map({"a": {"b": "v"}}))
print(namedtupled.json('{"a": {"b": "v"}}'))
print(namedtupled.yaml("a: a"))

os.environ['a'] = 'a'
os.environ['b'] = 'b'
print(namedtupled.env(['a', 'b']))

print(namedtupled.zip(['a', 'b'], ['a', 'b']))
