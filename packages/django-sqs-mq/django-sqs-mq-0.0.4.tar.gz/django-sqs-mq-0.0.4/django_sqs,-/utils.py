#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: utils.py
@ide: PyCharm
@time: 2020/4/1 12:07
@desc:
"""
import json


def is_json(js):
    try:
        json.loads(js)
    except ValueError:
        return False
    return True
