#!/usr/bin/env python
"""
fla.gr controller for viewing the logged in users profile

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute, route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youProfileTmpl import youProfileTmpl


@route("/your/profile")
@autoRoute()
class youProfile(baseHTMLObject):
    _title = "profile"
    __login__ = True
    def GET(self):
        """
        """
        view = youProfileTmpl(searchList=[self.tmplSearchList])
        return view
