#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Amlexa Package."""

import setuptools

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


setuptools.setup(
    name='amlexa',
    version='0.0.1b1',
    description='Amlexa - Amateur Radio Alexa.',
    license='Apache License, Version 2.0',
    author='Greg Albrecht',
    author_email='gba@orionlabs.io',
    zip_safe=False,
    packages=['amlexa'],
    install_requires=['requests >= 2.8.1'],
    entry_points={'console_scripts': ['amlexa = amlexa.cmd:cli']}
)
