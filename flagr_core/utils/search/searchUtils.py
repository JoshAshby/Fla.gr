#!/usr/bin/env python
"""
fla.gr aid for talking with the search daemon
"""
import config.config as c
import config.zmqBase as zmqc

import gevent

import logging
logger = logging.getLogger(c.logName+".searchUtils")


def _update(message):
    """
    Takes in a `message` and sends it out over zmq

    :param message: A str of the message to be sent over zmq
    :return: None
    """
    logger.debug("Sending signal: %s" % message)
    zmqc.zmqSock.send(message)
    logger.debug("Signal sent")


def updateSearch(man=False):
    """
    Triggers fla.gr's search index to be updated

    :param man: True or False for if this is a manual update
    """
    message = "flagIndexUpdate "
    if man:
        message += "now"
    else:
        message += "up"

    ser = gevent.spawn(_update, message)
    ser.join()
