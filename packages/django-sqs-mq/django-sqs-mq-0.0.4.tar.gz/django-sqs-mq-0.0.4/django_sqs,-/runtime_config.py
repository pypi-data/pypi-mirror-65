#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: runtime_config.py
@ide: PyCharm
@time: 2020/3/31 16:45
@desc:
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class RuntimeConfig:
    if not getattr(settings, 'AWS_ACCESS_KEY_ID'):
        raise ImproperlyConfigured('Missing setting "AWS_ACCESS_KEY_ID"')

    if not getattr(settings, 'AWS_SECRET_ACCESS_KEY'):
        raise ImproperlyConfigured('Missing setting "AWS_SECRET_ACCESS_KEY"')

    if not getattr(settings, 'AWS_DEFAULT_REGION'):
        raise ImproperlyConfigured('Missing setting "AWS_DEFAULT_REGION"')

    DEFAULTS = {
        'queue_name': settings.SQS_QUEUE_NAME,
        'sqs_queue_url': settings.SQS_QUEUE_URL,
        'aws_region_name': settings.AWS_DEFAULT_REGION,
        'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
    }

    @classmethod
    def get_conf_value(cls, key: str):

        # priority 0 are defaults
        if key in cls.DEFAULTS:
            return cls.DEFAULTS[key]

    @classmethod
    def get_sqs_queue_name(cls):
        return cls.get_conf_value('queue_name')

    @classmethod
    def get_sqs_queue_url(cls):
        return cls.get_conf_value('sqs_queue_url')

    @classmethod
    def get_access_key_id(cls):
        return cls.get_conf_value('aws_access_key_id')

    @classmethod
    def get_secret_access_key(cls):
        return cls.get_conf_value('aws_secret_access_key')

    @classmethod
    def get_region_name(cls):
        return cls.get_conf_value('aws_region_name')
