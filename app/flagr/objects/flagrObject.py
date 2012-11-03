#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import seshat.baseObject as bo
import flagr.views.flagrView as fv


class flagrObject(bo.baseHTTPObject):
    __name__ = "flagr"
    view = fv.flagrView
