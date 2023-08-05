#!/usr/bin/env python
# coding=utf-8
from setuptools import setup

setup(
        name='Hu_App',         # 应用名
        version='1.0',        # 版本号
        packages=['Hu_App'],    # 包括在安装包内的Python包
        install_requires=[
        'confluent_kafka'
    ],    
)
