#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: __init__.py
@ide: PyCharm
@time: 2020/3/31 15:11
@desc:
"""
import boto3
import logging
import boto3.session

from ..utils import is_json
from ..runtime_config import RuntimeConfig


logger = logging.getLogger('sqs_listener')


class SqsLauncher(object):

    def __init__(self):
        self._aws_region_name = RuntimeConfig.get_region_name()
        self._aws_access_key_id = RuntimeConfig.get_access_key_id()
        self._aws_secret_access_key = RuntimeConfig.get_secret_access_key()
        queue = RuntimeConfig.get_sqs_queue_name()
        queue_url = RuntimeConfig.get_sqs_queue_url()
        create_queue = False
        visibility_timeout = '600'

        self._session = boto3.session.Session()
        self._client = self._session.client(
            'sqs', region_name=self._aws_region_name,
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key
        )

        self._queue_name = queue
        self._queue_url = queue_url
        if not queue_url:
            queues = self._client.list_queues(QueueNamePrefix=self._queue_name)
            exists = False
            for q in queues.get('QueueUrls', []):
                qname = q.split('/')[-1]
                if qname == self._queue_name:
                    exists = True
                    self._queue_url = q

            if not exists:
                if create_queue:
                    q = self._client.create_queue(
                        QueueName=self._queue_name,
                        Attributes={
                            'VisibilityTimeout': visibility_timeout  # 10 minutes
                        }
                    )
                    self._queue_url = q['QueueUrl']
                else:
                    raise ValueError('No queue found with name ' + self._queue_name)
        else:
            self._queue_name = self._get_queue_name_from_url(queue_url)

    @staticmethod
    def _get_queue_name_from_url(url):
        return url.split('/')[-1]

    def send_message(self, message, **kwargs):
        """
        sends a message to the queue specified in the constructor
        :param message: (dict)
        :param kwargs:
        :return: (dict) the message response from SQS
        """
        if isinstance(message, str) and is_json(message) is None:
            raise ValueError('Message is not a valid json string')
        logger.info("Sending message to queue " + self._queue_name)
        if not kwargs:
            return self._client.send_message(
                QueueUrl=self._queue_url,
                MessageBody=message
            )
        return self._client.send_message(
            QueueUrl=self._queue_url,
            MessageBody=message,
            **kwargs
        )
