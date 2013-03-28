#!/usr/bin/env python
"""
main fla.gr index
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.adminIndexTmpl import adminIndexTmpl


@route("/admin")
class adminIndex(baseHTMLObject):
    """
    Returns base index page.
    """
    __name__ = "admin panel"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        Nothing much, just get the cheetah template for index and return it
        so Seshat can get cheetah to render it and then return it to the browser
        """
        view = adminIndexTmpl(searchList=[self.tmplSearchList])
        return view
