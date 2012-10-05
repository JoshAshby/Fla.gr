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


class baseResponse(object):
        def __init__(self, headers):
                self.status = headers[0]
                self.headers = headers[1]
