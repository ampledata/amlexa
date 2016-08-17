#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Alexa RSUV3 Utils."""

import os
import json
import re
import shlex
import subprocess
import time
import tempfile

import RPi.GPIO as gpio

import requests

import amlexa.constants

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


def tx_radio(media_path, response_path):


def tx_radio(media_path, response_path):
    #ptt_pin = amlexa.constants.PTT_PIN

    gpio.setmode(gpio.BCM)
    gpio.setup(18, gpio.OUT)

    gpio.output(18, False)
    time.sleep(1)
    amlexa.utils.play_audio(response_path)
    time.sleep(1)
    gpio.output(18, True)

    amlexa.utils.delete_media(media_path)
    amlexa.utils.delete_media(response_path)
