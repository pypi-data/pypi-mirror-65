#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Author:Jruing
# FileName:setup
# DateTime:2020/4/6 23:07
# SoftWare: PyCharm

from setuptools import setup
setup(name='DingDingBot',
      version='2.0',
      description='this is a dingdingbot packages',
      author='Jruing',
      author_email='1099301992@qq.com',
      packages=['DingDingBot'],
      requires=['requests'],
      python_requires='>=3'
      )