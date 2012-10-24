#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
routing decorator

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
from config import *

import seshat.baseURL as bu
import logging
logger = logging.getLogger("flagr.seshat.route")


def route(routeURL):
        def wrapper(HTTPObject):
                global urls
                urlObject = bu.url(routeURL, HTTPObject)
                urls.append(urlObject)
                HTTPObject.__url__ = routeURL
                if debug: logger.debug("""Made route table entry for:
        Object: %(objectName)s
        Pattern %(regex)s""" % {"regex": routeURL, "objectName": HTTPObject.__module__ + "." + HTTPObject.__name__})
                return HTTPObject
        return wrapper
