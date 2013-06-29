#!/usr/bin/env python
"""
main fla.gr index

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.objectMods import *
from seshat.route import autoRoute
from seshat.baseHTMLObject import baseHTMLObject


@autoRoute()
@admin()
class index(baseHTMLObject):
    """
    Returns base index page.
    """
    _title = "admin panel"
    _defaultTmpl = "flagpole/index/index"
    def GET(self):
        """
        Nothing much, just get the cheetah template for index and return it
        so Seshat can get cheetah to render it and then return it to the browser
        """
        return self.view
