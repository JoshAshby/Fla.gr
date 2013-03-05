#!/usr/bin/env python
"""
fla.gr main you dashboard controller

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youDashboardTmpl import youDashboardTmpl


@route("/you")
@route("/your/dashboard")
class youDashboard(baseHTMLObject):
    """
    """
    __name__="dashboard"
    def GET(self):
        """
        """
        view = youDashboardTmpl(searchList=[self.tmplSearchList])
        return view