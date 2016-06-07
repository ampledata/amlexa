#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Alexa Functions."""

import os
import json
import re
import shlex
import subprocess
import tempfile

import requests

import amlexa.constants

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


def get_token():
    response = None
    payload = {
        'client_id': amlexa.constants.CLIENT_ID,
        'client_secret': amlexa.constants.CLIENT_SECRET,
        'refresh_token': amlexa.constants.REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }
    response = requests.post(amlexa.constants.OAUTH_URL, data=payload)
    if response is not None and response.ok:
        response_text = json.loads(response.text)
        if 'access_token' in response_text:
            return response_text['access_token']


def alexa(input_path):
    response = None
    boundary = None
    audio = None

    headers = {'Authorization': 'Bearer %s' % get_token()}

    with open(input_path) as inf:
        files = [
            ('file', ('request', json.dumps(amlexa.constants.ALEXA_PAYLOAD),
                'application/json; charset=UTF-8')),
            ('file', ('audio', inf, 'audio/L16; rate=16000; channels=1'))
        ]
        response = requests.post(
            amlexa.constants.REC_URL, headers=headers, files=files)
        print response

    if response is not None and response.ok and response.status_code == 200:

        for header in response.headers['content-type'].split(';'):
            if re.match('.*boundary.*', header):
                boundary = header.split('=')[1]

        if boundary is not None:
            response_data = response.content.split(boundary)
            for data_chunk in response_data:
                if len(data_chunk) >= 1024:
                    audio = data_chunk.split('\r\n\r\n')[1].rstrip('--')

        if audio is not None:
            tmp_fd, mp3_path = tempfile.mkstemp(
                prefix='amlexa', suffix='.mp3')
            os.close(tmp_fd)

            with open(mp3_path, 'wb') as mp3_fd:
                mp3_fd.write(audio)

            return mp3_path
