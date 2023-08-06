#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Mark
# Mail: 1782980833@qq.com
# Created Time:  2020-3-29 16:00:00
#############################################

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="ForMark",  # 这里是pip项目发布的名称
    version="1.1.1",  # 版本号，数值大的会优先被pip
    keywords=("pip", "ForMark", "mark"),
    description="工具类整理",
    long_description="https://www.handsomemark.com/",
    license="MIT Licence",
    url="https://github.com/zhaolixiang/ForMark",  # 项目相关文件地址，一般是github
    author="Mark",
    author_email="1782980833@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["flask","loguru","tls-sig-api-v2",
                      "requests","pycryptodome","oss2",
                      "mongoengine","Pillow","pycodestyle",
                      "pymongo","urllib3","qrcode","twine","pymysql","flask_cors"]  # 这个项目需要的第三方库
)
