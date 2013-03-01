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

        """
        view = indexTmpl(searchList=[self.tmplSearchList])
        return view
