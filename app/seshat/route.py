#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
routing decorator

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

import baseURL as bu
import logging
logger = logging.getLogger("seshat.seshat.route")


def route(routeURL):
        def wrapper(HTTPObject):
                urlObject = bu.url(routeURL, HTTPObject)
                c.urls.append(urlObject)
                HTTPObject.__url__ = routeURL
                if c.debug: logger.debug("""Made route table entry for:
        Object: %(objectName)s
        Pattern %(regex)s""" % {"regex": routeURL, "objectName": HTTPObject.__module__ + "." + HTTPObject.__name__})
                return HTTPObject
        return wrapper
