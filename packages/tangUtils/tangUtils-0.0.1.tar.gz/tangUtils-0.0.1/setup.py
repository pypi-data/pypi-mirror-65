#!/usr/bin/env python
# coding: utf-8

"""
see https://pypi.org/project/twine/
"""

from setuptools import setup

setup(
    name='tangUtils',
    version='0.0.1',
    author='xiaomingtang',
    author_email='1038761793@qq.com',
    url='https://upload.pypi.org/legacy/tangUtils',
    description=u'文件/目录相关utils',
    packages=['tangUtils'],
    install_requires=[
      "pillow"
    ],
    entry_points={
        'console_scripts': [
        ]
    }
)