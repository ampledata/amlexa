#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Amlexa Constants."""

import logging
import os

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = logging.Formatter(
    '%(asctime)s amlexa %(levelname)s %(name)s.%(funcName)s:%(lineno)d '
    '- %(message)s')

PRODUCT_ID = os.environ.get('PRODUCT_ID', 'PRODUCT_ID')
SECURITY_PROFILE_DESCRIPTION = os.environ.get(
    'SECURITY_PROFILE_DESCRIPTION', 'SECURITY_PROFILE_DESCRIPTION')
SECURITY_PROFILE_ID  = os.environ.get('SECURITY_PROFILE_ID', 'SECURITY_PROFILE_ID')
CLIENT_ID = os.environ.get('CLIENT_ID', 'CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', 'CLIENT_SECRET')

REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN', 'REFRESH_TOKEN')

OAUTH_URL = 'https://api.amazon.com/auth/o2/token'
REC_URL = 'https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize'

ALEXA_PAYLOAD = {
    'messageHeader': {
        'deviceContext': [
            {
                'name': 'playbackState',
                'namespace': 'AudioPlayer',
                'payload': {
                    'streamId': '',
                    'offsetInMilliseconds': '0',
                    'playerActivity': 'IDLE'
                }
            }
        ]
    },
    'messageBody': {
        'profile': 'alexa-close-talk',
        'locale': 'en-us',
        'format': 'audio/L16; rate=16000; channels=1'
    }
}
