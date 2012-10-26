#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
response container

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""


class baseResponse(object):
        def __init__(self, headers):
                self.status = headers[0]
                self.headers = headers[1]
