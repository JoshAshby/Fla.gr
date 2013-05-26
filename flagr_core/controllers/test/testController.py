#!/usr/bin/env python
"""
main fla.gr test page

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject


@autoRoute()
class testIndex(baseHTMLObject):
    """
    Returns bare test page.
    """
    def GET(self):
        endName = self.__module__.split(".")
        name = endName[len(endName)-1]
        return name


@autoRoute()
class testSave(baseHTMLObject):
    def GET(self):
        return "Hello"
