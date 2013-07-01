#!/usr/bin/env python
"""
fla.gr controller for view a list of current flags and status

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import *

from models.couch.user.userModel import userORM
from models.couch.flag.flagModel import flagORM
import models.couch.baseCouchCollection as bcc

from views.template import listView, paginateView


@autoRoute()
@admin()
class index(HTMLObject):
    _title = "flagpole flags"
    _defaultTmpl = "flagpole/flags/flags"
    def GET(self):
        """
        """
        page = self.request.getParam("page", 1)
        perpage = self.request.getParam("perpage", 25)
        sort = self.request.getParam("sort", "title")

        flags = bcc.baseCouchCollection(flagORM)
        flags.paginate(page, perpage)
        flags.fetch()
        flags.format()
        flags.join(userORM, "userID")
        flags.sortBy(sort)

        flagsList = listView("flagpole/partials/rows/flag", flags)
        pagination = paginateView(flags)

        self.view.data = {"flags" : flagsList,
            "pagination": pagination}

        return self.view
