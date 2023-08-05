#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 04/10/2019
"""

from setuptools import setup

setup(name='m-license',
      version='1.7',
      description='Mobio libraries',
      url='https://github.com/mobiovn',
      author='MOBIO',
      author_email='contact@mobio.vn',
      license='MOBIO',
      packages=['mobio/libs/license'],
      package_data={'': ['*.so']},
      install_requires=['python-jose',
                        'pycryptodome==3.4.3',
                        'numpy'])
