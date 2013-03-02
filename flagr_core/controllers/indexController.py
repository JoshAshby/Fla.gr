#!/usr/bin/env python
"""
main fla.gr index

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
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
