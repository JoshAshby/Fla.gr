#!/usr/bin/env python
"""
fla.gr controller for viewing the logged in users flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youProfileTmpl import youProfileTmpl


@route("/your/profile")
class adminUsers(baseHTMLObject):
    __name__ = "profile"
    def GET(self):
        """
        """
        view = youProfileTmpl(searchList=[self.tmplSearchList])

        return view
