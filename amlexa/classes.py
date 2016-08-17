#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Amlexa Classes."""

import logging
import os
import threading

import requests

import amlexa.functions
import amlexa.utils

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


class AmlexaListenerThread(threading.Thread):

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(amlexa.constants.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(amlexa.constants.LOG_LEVEL)
        _console_handler.setFormatter(amlexa.constants.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, media_dir, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.media_dir = media_dir
        self.queue = queue
        self._stop = threading.Event()

    def stop(self):
        """Stop the thread at the next opportunity."""
        self._stop.set()

    def stopped(self):
        """Checks if the thread is stopped."""
        return self._stop.isSet()

    def run(self):
        self._logger.info('Running Thread: Listener')
        while not self.stopped():
            self._logger.debug(
                'Starting recording at media_dir=%s', self.media_dir)
            media_path = amlexa.utils.vox_record_audio(self.media_dir)
            try:
                if os.stat(media_path).st_size > 0:
                    self._logger.debug(
                        'Completed recording at media_path=%s', media_path)
                    self.queue.put(media_path)
                else:
                    self._logger.error(
                        'Empty recording at media_path=%s', media_path)
            except OSError:
                self._logger.error('No recording at media_path=%s', media_path)


class AmlexaResponderThread(threading.Thread):

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(amlexa.constants.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(amlexa.constants.LOG_LEVEL)
        _console_handler.setFormatter(amlexa.constants.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, media_dir, queue, callback=None):
        threading.Thread.__init__(self)
        self.daemon = True
        self.media_dir = media_dir
        self.queue = queue
        self.callback = callback
        self._stop = threading.Event()

    def stop(self):
        """Stop the thread at the next opportunity."""
        self._stop.set()

    def stopped(self):
        """Checks if the thread is stopped."""
        return self._stop.isSet()

    def run(self):
        self._logger.info('Running Thread: Responder')

        while not self.stopped():
            media_path = self.queue.get()
            self._logger.debug('Dequeued media_path=%s', media_path)

            if os.path.exists(media_path):
                self._logger.debug('Processing media_path=%s', media_path)
                response_path = amlexa.functions.alexa(media_path)

                if response_path is not None:
                    if self.callback is not None:
                        self.callback(media_path, response_path)
                    else:
                        self._logger.debug(
                            'Playing response_path=%s', response_path)
                        amlexa.utils.play_audio(response_path)

                        self._logger.debug(
                            'Deleting media_path=%s', media_path)
                        amlexa.utils.delete_media(media_path)

                        self._logger.debug(
                            'Deleting response_path=%s', response_path)
                        amlexa.utils.delete_media(response_path)
            self.queue.task_done()
