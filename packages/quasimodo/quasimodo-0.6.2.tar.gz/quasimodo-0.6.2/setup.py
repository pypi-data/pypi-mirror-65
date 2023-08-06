#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import versioneer

setup(
    name='quasimodo',
    author="doubleO8",
    author_email="wb008@hdm-stuttgart.de",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="no description",
    long_description="no long description either",
    url="https://localhost/quasimodo",
    packages=['quasimodo'],
    install_requires=[
        'pika>=1.1.0',
        'paho-mqtt>=1.5.0'
    ],
    entry_points={
        'console_scripts': [
            'quasimonkey = quasimodo.hunchback:hunchback_client',
        ]
    }
)
