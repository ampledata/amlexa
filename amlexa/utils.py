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


def vox_record_audio(audio_dir):
    """
    Records VOX audio via sound-card input.

    :param audio_dir: Destination directory for audio recording.
    :type audio_dir: str
    :returns: Path to Audio File.
    :rtype: str
    """
    tmp_fd, audio_path = tempfile.mkstemp(
        prefix='vox_record_audio_', suffix='.wav', dir=audio_dir)
    os.close(tmp_fd)

    rec_cmd = "rec -r 16k -b 16 -c 1 -q %s silence 1 0.1 3%% 1 3.0 3%%" % audio_path
    rec_args = shlex.split(rec_cmd)
    rec_proc = subprocess.Popen(
        rec_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rec_proc.communicate()

    if os.path.exists(audio_path) and os.stat(audio_path).st_size is not 0:
        return audio_path


def play_audio(audio_file):
    """
    Plays audio file out of default audio device.
    """
    aplay_cmd = ' '.join(['play', audio_file])
    aplay_args = shlex.split(aplay_cmd)
    aplay_proc = subprocess.Popen(aplay_args)
    aplay_proc.wait()
    return aplay_proc



def delete_media(media_path):
    """
    Deletes media file at path (to save space).

    :param media_path: Path to Media File.
    :type media_path: str
    """
    return os.unlink(media_path)
