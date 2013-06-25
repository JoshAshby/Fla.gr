#!/usr/bin/env python
"""
fla.gr main you dashboard controller
Does nothing right now

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.you.youDashboardTmpl import youDashboardTmpl


@autoRoute()
class youIndex(baseHTMLObject):
    """
    """
    _title ="dashboard"
    __login__ = True
    def GET(self):
        """
        """
        view = youDashboardTmpl(searchList=[self.tmplSearchList])
        return view
