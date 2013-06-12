#!/usr/bin/env python
"""
Controller for searching through items in fla.gr

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

import utils.search.flag.flagSearch as fs

from views.searchTmpl import searchTmpl
from views.partials.flags.flagsListTmpl import flagsListTmpl


@autoRoute()
class search(baseHTMLObject):
    _title = "search"
    def GET(self):
        if self.env["cfg"].enablePublicPages and self.env["cfg"].enablePublicSearch:
            page = self.env["members"]["p"] if self.env["members"].has_key("p") else 1
            value = self.env["members"]["s"] if self.env["members"].has_key("s") else ""

            flags = fs.flagSearch(value)

            view = searchTmpl(searchList=[self.tmplSearchList])

            if self.env["cfg"].enableModalFlagDeletes:
                view.scripts = ["handlebars_1.0.min",
                        "jquery.json-2.4.min",
                        "adminModal.flagr",
                        "editForm.flagr",
                        "deleteFlagModal.flagr"]

            flagsTmpl = flagsListTmpl(searchList=[self.tmplSearchList])
            flagsTmpl.flags = flags

            view.flagResults = str(flagsTmpl)
            view.query = value

            return view
        else:
            self._404()
