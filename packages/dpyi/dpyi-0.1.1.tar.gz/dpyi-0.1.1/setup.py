#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: huaqingyi
# Mail: 2304816231@qq.com
# Created Time:  2020-04-12 19:50:34
#############################################


from setuptools import setup, find_packages

setup(
    name="dpyi",
    version="0.1.1",
    keywords=("pip", "rest", "controller", "dpyi", "django"),
    description="django controller and dto service",
    long_description="django mvt to mvc",
    license="MIT Licence",

    url="https://github.com/huaqingyi/dpyi",
    author="huaqingyi",
    author_email="2304816231@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'djangorestframework', 'django'
    ]
)
