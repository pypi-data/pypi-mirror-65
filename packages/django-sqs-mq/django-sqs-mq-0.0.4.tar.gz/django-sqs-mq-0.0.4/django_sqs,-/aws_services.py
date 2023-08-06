#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: aws_services.py
@ide: PyCharm
@time: 2020/4/7 15:59
@desc:
"""
import boto3


def aws_connect(service_name, region="us-east-1"):
    try:
        client = boto3.client(service_name, region_name=region)
        return client
    except Exception as e:
        raise Exception(f"Could not connect to AWS resources {e}")


def send_message(aws_conn, queue_url, message):
    try:
        response = aws_conn.send_message(QueueUrl=queue_url, MessageBody=message)
        if "200" not in str(response.get("ResponseMetadata").get("HTTPStatusCode")):
            raise Exception("Error sending message")

        return True
    except Exception as e:
        raise e


def recive_messages(aws_conn, queue_url):
    message_dict = {}
    try:
        response = aws_conn.receive_message(QueueUrl=queue_url, AttributeNames=["All"])
        if not response.get("Messages"):
            return False
        reciptHandler = response.get("Messages")[0].get("ReceiptHandle")
        message = response.get("Messages")[0].get("Body")
        message_dict["message"] = {"messageKey": reciptHandler, "body": message}
        return message_dict
    except Exception as e:
        raise e


def delete_message(aws_conn, queue_url, reciptHandler):
    try:
        response = aws_conn.delete_message(
            QueueUrl=queue_url, ReceiptHandle=reciptHandler
        )
        return response
    except Exception as e:
        raise e


def sqs_list_queues(aws_conn, prefix_name):
    response = aws_conn.list_queues(QueueNamePrefix=prefix_name)

    return response
