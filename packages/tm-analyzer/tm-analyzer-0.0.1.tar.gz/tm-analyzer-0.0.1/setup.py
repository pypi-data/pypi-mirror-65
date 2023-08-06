#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 5:41 下午
# @Author  : kewen
# @File    : setup.py.py

from setuptools import setup, find_packages

setup(
    name='tm-analyzer',
    version='0.0.1',
    author='zkwlx',
    author_email='xuzhi@bytedance.com',
    url='',
    description='A powerful tool to help Android engineers optimize their performance',
    packages=find_packages(),
    install_requires=['bokeh'],
    entry_points={
        'console_scripts': [
            'tm-analyzer=main.analyzer:main'
        ]
    },
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3 :: Only',
    ],
)
