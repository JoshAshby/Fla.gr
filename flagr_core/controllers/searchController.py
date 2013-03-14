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
import config.config as c

from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import search.flag.flagSearch as fs

from views.searchTmpl import searchTmpl

import utils.pagination as p
import config.dbBase as db
from models.user.userModel import userORM


@route("/search")
class searchController(baseHTMLObject):
    __name__ = "search"
    def GET(self):
        page = self.env["members"]["p"] if self.env["members"].has_key("p") else 1
        value = self.env["members"]["s"] if self.env["members"].has_key("s") else ""

        flagResults = fs.flagSearch(value)

        view = searchTmpl(searchList=[self.tmplSearchList])

        for flag in flagResults:
            flag.author = userORM.load(db.couchServer, flag.userID)

        flagResults = p.pagination(flagResults, 10, int(page))

        view.flagResults = flagResults
        view.query = value

        return view
