# -*- coding: utf-8 -*-
__author__ = 'XQ'

# !/usr/bin/env python

#############################################
# File Name: setup.py
# Author: XQ
# Mail: 5273508@qq.com
# Created Time:  2020-04-07
#############################################

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="xq_common",  # 这里是pip项目发布的名称
    version="1.0.0.1",  # 版本号，数值大的会优先被pip
    keywords=("pip", "common"),
    description="xq common",
    long_description="",
    license="MIT Licence",
    url="",  # 项目相关文件地址，一般是github
    author="XQ",
    author_email="5273508@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms='python 3.7',
    install_requires=[],  # 这个项目需要的第三方库
)
