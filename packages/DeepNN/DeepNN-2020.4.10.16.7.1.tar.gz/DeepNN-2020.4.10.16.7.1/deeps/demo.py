#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : DeepTricks.
# @File         : demo
# @Time         : 2019-09-10 15:17
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from yaml import safe_load

print(safe_load(open('./files.yml')))

from tensorflow.python.keras.preprocessing import text
from tensorflow.python.keras.preprocessing.text import hashing_trick


text.Tokenizer

from tensorflow.keras.preprocessing import text