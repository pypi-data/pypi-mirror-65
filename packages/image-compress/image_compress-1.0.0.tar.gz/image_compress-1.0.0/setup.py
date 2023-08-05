#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: wanghaun
# Mail: wanghaun0718@outlook.com
# Created Time:  2020-4-02 10:29:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "image_compress",
    version = "1.0.0",
    keywords = ["pip", "image","compress", "wanghuan"],
    description = "Image compress tool",
    long_description = "",
    license = "MIT Licence",

    author = "wanghuan",
    author_email = "wanghuan0718@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)