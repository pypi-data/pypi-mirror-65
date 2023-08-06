#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: parse_message.py
@ide: PyCharm
@time: 2020/4/7 16:01
@desc:
"""


def parse_message(message):
    message_dict = {}

    message = message.replace("{", "")
    message = message.replace("}", "")
    splited_message = message.split("\n")

    try:
        for field in splited_message:
            message_not_splited = field.strip()
            tranformed_message = message_not_splited.split(":")

            if tranformed_message[0]:
                key = tranformed_message[0].replace('"', "")
                value = tranformed_message[1].replace('"', "")
                key_cleaned = key.replace("“", "").replace("”", "")
                value_cleaned = value.replace("“", "").replace("”", "")
                if "," in value_cleaned[-1]:
                    value_cleaned = value_cleaned.replace(",", "")
                message_dict[key_cleaned] = value_cleaned
        return message_dict
    except Exception as e:
        raise e
