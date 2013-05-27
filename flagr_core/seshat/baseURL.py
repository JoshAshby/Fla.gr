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
        self.url = urlStr
        self.regex = re.compile("^" + self.url +"(|.json|/)$")
        self.pageObject = pageObject
        self.name = pageObject.__name__ or "unnamedFalgrPage"


class autoURL(object):
    def __init__(self, pageObject):
        fullModule = pageObject.__module__
        bits = fullModule.split(".")
        bases = []
        for bit in bits[1:]:
            if len(bit.split("Controller")) > 1:
                break;
            else:
                bases.append(bit.lower())

        self.url = "/"
        space = ""
        for base in bases:
            if bases.index(base) > 0:
                space += base.capitalize()
            else:
                space += base.lower()
            self.url += base + "/"

        splitName = pageObject.__name__.split(space)
        name = splitName[len(splitName)-1].lower()

        if name == "index":
            self.url = self.url.rstrip("/")
            self.preRegex = "^" + self.url + "(?:|/)$"
        else:
            self.url += name
            self.preRegex = "^" + self.url +"(?:|/(.*))(?:|/)$"

        self.regex = re.compile(self.preRegex)
        self.pageObject = pageObject
        self.name = pageObject.__name__ or "unnamedFalgrPage"
