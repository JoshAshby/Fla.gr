#!/usr/bin/env python
"""
fla.gr maintenance controller
Catches all URLS
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
