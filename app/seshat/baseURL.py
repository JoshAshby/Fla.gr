#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
route table container

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import re


class url(object):
        """
        Base container for storing the pre regex url, regex, and object
        which gets entered into the route table.
        """
        def __init__(self, urlStr, pageObject):
                self.regex = re.compile("^" + urlStr + "$")
                self.url = urlStr
                self.pageObject = pageObject
                self.name = pageObject.__menu__
