#!/usr/bin/env python
"""
fla.gr main you dashboard controller
Does nothing right now besides presenting a quick flag box, and to act as a landing page
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
    __login__ = True
    def GET(self):
        """
        """
        view = youDashboardTmpl(searchList=[self.tmplSearchList])
        return view
