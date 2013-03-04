#!/usr/bin/env python2
"""
fla.gr controller for authentication login

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.users.adminViewUsersTmpl import adminViewUsersTmpl

import config.dbBase as db
from models.user.userModel import userORM


@route("/admin/users")
class adminUsers(baseHTMLObject):
    __name__ = "admin users"
    __level__ = 50
    def GET(self):
        """
        """
        view = adminViewUsersTmpl(searchList=[self.tmplSearchList])

        users = userORM.view(db.couchServer, 'typeViews/user')
        for user in users:
            if user > self.session.level:
                users.pop(users.index(user))
        view.users = users

        return view
