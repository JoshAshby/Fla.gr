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
