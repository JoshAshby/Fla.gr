#!/usr/bin/env python
"""
main fla.gr error pages
"""
from utils.baseHTMLObject import baseHTMLObject

from views.errorTmpl import errorTmpl


class error404(baseHTMLObject):
    """
    Returns base 404 error page.
    """
    __name__ = "404 Not Found"
    def GET(self):
        """
        """
        self.head = ("404 NOT FOUND", [("Content-Type", "text/html")])
        view = errorTmpl(searchList=[self.tmplSearchList])
        return view
