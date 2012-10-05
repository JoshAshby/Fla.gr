#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
from config import *

import re


class url(object):
        def __init__(self, urlStr, pageObject):
                self.regex = re.compile("^" + urlStr + "$")
                self.url = urlStr
                self.pageObject = pageObject
