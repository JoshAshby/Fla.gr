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
import config.config as c

import baseURL as bu
import logging
logger = logging.getLogger(c.logName+".seshat.route")


def route(routeURL, urls=c.urls):
        def wrapper(HTTPObject):
                urlObject = bu.url(routeURL, HTTPObject)
                urls.append(urlObject)
                HTTPObject.__url__ = routeURL
                if c.debug: logger.debug("""Made route table entry for:
        Object: %(objectName)s
        Pattern %(regex)s""" % {"regex": routeURL, "objectName": HTTPObject.__module__ + "." + HTTPObject.__name__})
                return HTTPObject
        return wrapper
