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


@autoRoute()
class adminUsersIndex(baseHTMLObject):
    _title = "admin users"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        view = adminViewUsersTmpl(searchList=[self.tmplSearchList])

        users = userORM.all()
        #Don't let you see people higher than you,
        #just out of safety for them...
        for user in users:
            if user.level > self.session.level:
                users.rows.pop(users.rows.index(user))
        view.users = users

        return view
