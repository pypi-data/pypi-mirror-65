#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import versioneer

setup(
    name='djali',
    author="doubleO8",
    author_email="wb008@hdm-stuttgart.de",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="no description",
    long_description="no long description either",
    url="https://localhost/djali",
    packages=['djali'],
    install_requires=[
        'six>=1.13.0',
        'cloudant>=2.12.0',
    ],
    extras_require={
        "dynamodb":  [
            "boto3>=1.12.38",
        ],
    }
)
