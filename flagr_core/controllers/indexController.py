#!/usr/bin/env python
"""
main fla.gr index
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.indexTmpl import indexTmpl


@route("/")
class index(baseHTMLObject):
    """
    Returns base index page.
    """
    __name__ = "home"
    def GET(self):
        """
        Nothing much, just get the cheetah template for index and return it
        so Seshat can get cheetah to render it and then return it to the browser
        """
        view = indexTmpl(searchList=[self.tmplSearchList])
        return view
