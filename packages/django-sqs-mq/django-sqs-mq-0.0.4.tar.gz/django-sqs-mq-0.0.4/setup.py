#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: sun
@license: (C) Copyright 2016-2019, Light2Cloud (Beijing) Web Service Co., LTD
@contact: wenhaijie@light2cloud.com
@software: L2CloudCMP
@file: setup.py.py
@ide: PyCharm
@time: 2020/4/1 13:22
@desc:
"""
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="django-sqs-mq",
    version="0.0.4",
    author="whj",
    author_email="whj@linuxbs.com",
    description="A simple wrapper for boto3 for receive, and sending, to an AWS SQS queue.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/firestarry/django-sqs.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'django>=1.11.29',
        'boto3>=1.12.33'
    ],
    zip_safe=True,
    python_requires='>=3.6',

)
