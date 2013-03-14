#!/usr/bin/env python2
"""
fla.gr maintenance controller
Catches all URLS

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route

from utils.baseHTMLObject import baseHTMLObject

from views.maintenanceTmpl import maintenanceTmpl


@route("/(.*)")
class maintenance(baseHTMLObject):
    """
    Returns base maintenance page
    """
    __name__ = "maintenance"
    def GET(self):
        """

        """
        view = maintenanceTmpl(searchList=[self.tmplSearchList])
        return view
