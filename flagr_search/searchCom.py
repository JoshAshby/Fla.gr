#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

Flagr related tasks and config options.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import siteConfig.zmqConfig as zmqc

import gevent

import logging
logger = logging.getLogger(c.logName+".flagrConfig")

def _update(message):
    logger.debug("Sending signal: %s" % message)
    zmqc.zmqSock.send(message)
    logger.debug("Signal sent")

def updateSearch(man=False):
    message = "indexUpdate "
    if man:
        message += "now"
    else:
        message += "increase"

    ser = gevent.spawn(_update, message)
    ser.join()
