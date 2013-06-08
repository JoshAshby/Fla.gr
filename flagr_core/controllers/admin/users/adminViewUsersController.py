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
from utils.baseHTMLObject import baseHTMLObject

from views.admin.users.adminViewUsersTmpl import adminViewUsersTmpl

from models.couch.user.userModel import userORM
import models.couch.baseCouchCollection as bcc


@autoRoute()
class adminUsersIndex(baseHTMLObject):
    _title = "admin users"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        page = self.env["members"]["p"] \
                if self.env["members"].has_key("p") else 1
        view = adminViewUsersTmpl(searchList=[self.tmplSearchList])

        users = bcc.baseCouchCollection(userORM)
        users.paginate(page, 25)
        users.fetch()
        users.format()

        view.users = users

        return view
