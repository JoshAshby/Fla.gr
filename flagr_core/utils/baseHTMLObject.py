#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.baseObject import baseHTTPObject

import models.bucket.bucketModel as bm

class baseHTMLObject(baseHTTPObject):
    def finishInit(self):
        try:
            self.__name__ = self.__name__
        except:
            self.__name__ = "untitledFlagrPage"

        self.head = ("200 OK", [("Content-Type", "text/html")])
        self.env["cfg"] = bm.cfgBuckets()
        self.tmplSearchList = {"user": self.session,
                "page": (self.__name__),
                "cfg": self.env["cfg"],
                "flagrCoreScripts": ["main.flagr"]}
