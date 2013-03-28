#!/usr/bin/env python
"""
Controller for searching through personal flags for a user
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import utils.search.flag.flagSearch as fs

from views.searchTmpl import searchTmpl

import utils.pagination as p


@route("/your/search")
class youSearchController(baseHTMLObject):
    __name__ = "your search"
    def GET(self):
        page = self.env["members"]["p"] if self.env["members"].has_key("p") else 1
        value = self.env["members"]["s"] if self.env["members"].has_key("s") else ""

        flagResults = fs.flagSearch(value)

        view = searchTmpl(searchList=[self.tmplSearchList])

        for flag in flagResults:
            if flag.userID != self.session.id:
                flagResults.pop(flagResults.index(flag))

        flagResults = p.pagination(flagResults, 10, int(page))

        view.flagResults = flagResults
        view.query = value

        return view
