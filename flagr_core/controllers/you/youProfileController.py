#!/usr/bin/env python
"""
fla.gr controller for viewing the logged in users profile
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youProfileTmpl import youProfileTmpl


@route("/your/profile")
class youProfile(baseHTMLObject):
    __name__ = "profile"
    __login__ = True
    def GET(self):
        """
        """
        view = youProfileTmpl(searchList=[self.tmplSearchList])
        return view
