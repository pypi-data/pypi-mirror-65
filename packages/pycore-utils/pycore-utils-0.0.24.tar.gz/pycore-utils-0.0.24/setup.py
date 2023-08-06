#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

setup(
    name='pycore-utils',
    version='0.0.24',
    author='pycore',
    author_email='pycore_team@gmail.com',
    description='python utils',
    packages=find_packages(), install_requires=['pymysql', 'redis']
)
