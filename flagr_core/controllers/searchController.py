#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

You controller. Everything under the /you
        URL is handled and fleshed out, or linked to
        from here.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c

from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

#import search.flag.flagSearch as fs

from views.searchTmpl import searchTmpl


@route("/search/flags")
class searchFlagsController(baseHTMLObject):
    def GET(self):
        value = self.env["members"]["s"] if self.env["members"].has_key("s") else ""

#        results = fs.search(value)

        view = searchTmpl(searchList=[self.tmplSearchList])

#        view.results = results

        return view
