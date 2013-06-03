#!/usr/bin/env python
"""
fla.gr aid for talking with the search daemon

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c

import gevent

import logging
logger = logging.getLogger(c.general.logName+".searchUtils")


def _update(message):
    """
    Takes in a `message` and sends it out over zmq

    :param message: A str of the message to be sent over zmq
    :return: None
    """
    logger.debug("Sending signal: %s" % message)
    c.zeromq.socket.send(message)
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
