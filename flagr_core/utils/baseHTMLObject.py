#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

This is an extension of baseHTTPObject designed for fla.gr to be able to easily
return HTML pages
"""
from seshat.baseObject import baseHTTPObject

import models.bucket.bucketModel as bm

class baseHTMLObject(baseHTTPObject):
    def finishInit(self):
        """
        Sets up some fla.gr specific HTML page items within each page object
        """
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
