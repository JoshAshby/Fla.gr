#!/usr/bin/env python
"""
fla.gr aid for talking with the search daemon

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c
import config.zmqConfig as zmqc

import gevent

import logging
logger = logging.getLogger(c.logName+".flagrSearch")

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
    message = "indexUpdate "
    if man:
        message += "now"
    else:
        message += "increase"

    ser = gevent.spawn(_update, message)
    ser.join()
