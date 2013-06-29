#!/usr/bin/env python
"""
fla.gr controller for view a list of current users

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseHTMLObject import baseHTMLObject
from seshat.objectMods import *

from models.couch.user.userModel import userORM
import models.couch.baseCouchCollection as bcc

from views.template import listView, paginateView


@autoRoute()
@admin()
class index(baseHTMLObject):
    _title = "flagpole users"
    _defaultTmpl = "flagpole/users/users"
    def GET(self):
        """
        """
        page = self.request.getParam("page", 1)
        perpage = self.request.getParam("perpage", 25)
        sort = self.request.getParam("sort", "username")

        users = bcc.baseCouchCollection(userORM)
        users.paginate(page, perpage)
        users.fetch()
        users.format()
        users.sortBy(sort)

        usersList = listView("flagpole/partials/rows/user", users)
        pagination = paginateView(users)

        self.view.data = {"users": usersList,
            "pagination": pagination}

        return self.view
