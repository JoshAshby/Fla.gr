#!/usr/bin/env python
"""
main fla.gr error pages

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from utils.baseHTMLObject import baseHTMLObject

from views.error.error404Tmpl import error404Tmpl
from views.error.error500Tmpl import error500Tmpl


class error404(baseHTMLObject):
    """
    Returns base 404 error page.
    """
    _title = "404 NOT FOUND"
    def GET(self):
        """
        """
        self.head = ("404 NOT FOUND", [("Content-Type", "text/html")])
        view = error404Tmpl(searchList=[self.tmplSearchList])
        return view


class error500(baseHTMLObject):
    """
    Returns base 500 error page.
    """
    _title = "500 INTERNAL SERVER ERROR"
    def GET(self):
        """
        """
        self.head = ("500 INTERNAL SERVER ERROR", [("Content-Type", "text/html")])
        view = error500Tmpl(searchList=[self.tmplSearchList])
        view.error = self.env["members"]["error"]
        return view
