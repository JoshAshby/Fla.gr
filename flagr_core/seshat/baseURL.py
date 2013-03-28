#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
route table container
"""
import re


class url(object):
        """
        Base container for storing the pre regex url, regex, and object
        which gets entered into the route table.
        """
        def __init__(self, urlStr, pageObject):
                self.regex = re.compile("^" + urlStr +"(|.json|/)$")
                self.url = urlStr
                self.pageObject = pageObject
                self.name = pageObject.__name__ or "unnamedFalgrPage"
