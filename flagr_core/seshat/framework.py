#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Main framework app

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
from gevent import monkey; monkey.patch_all()

import config.config as c

import gevent
from gevent_fastcgi.server import WSGIServer

import logging
logger = logging.getLogger(c.logName+".seshat")

from seshat.coreApp import app


def main():
        """
        Server

        Sets up the server and all that messy stuff
        """
        if c.port and type(c.port) is str:
                port = int(c.port)
        else:
                port = 8000
        if not c.address:
                address = "127.0.0.1"
        else:
                address = c.address

        server = WSGIServer((address, port), app)

        logger.info("""Now serving py as a fastcgi server at %(address)s:%(port)i
        Press Ctrl+c if running as non daemon mode, or send a stop signal
        """ % {"address": address, "port": port})

        return server


def serveForever():
        """
        Server

        Starts the server
        """
        server = main()
        try:
                server.serve_forever()
                logger.warn("Shutdown py operations.")
        except Exception as exc:
                logger.critical("""Shutdown py operations, here's why: %s""" % exc)
                gevent.shutdown
        except KeyboardInterrupt:
                logger.critical("""Shutdown py operations for a KeyboardInterrupt. Bye!""")
                gevent.shutdown
        else:
                logger.critical("""Shutdown py operations for unknown reason, possibly a KeyboardInterrupt...""")
                gevent.shutdown
