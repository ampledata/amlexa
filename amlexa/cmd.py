#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Amlexa Commands."""

import argparse
import Queue
import time

import amlexa
import amlexa.constants
import amlexa.rsuv3

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.io>'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'
__license__ = 'Apache License, Version 2.0'


def cli():
    """Command Line interface for Amlexa."""

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--media_dir', help='Media Dir', default=None)
    opts = parser.parse_args()

    queue = Queue.Queue()
    worker_listen = amlexa.AmlexaListenerThread(opts.media_dir, queue)
    worker_respond = amlexa.AmlexaResponderThread(
        opts.media_dir, queue, callback=amlexa.rsuv3.tx_radio)

    try:
        worker_listen.start()
        worker_respond.start()
        queue.join()
        while worker_listen.is_alive() and worker_respond.is_alive():
            time.sleep(0.01)
    except KeyboardInterrupt:
        worker_listen.stop()
        worker_respond.stop()
    finally:
        worker_listen.stop()
        worker_respond.stop()


if __name__ == '__main__':
    cli()
