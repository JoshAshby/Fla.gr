#!/usr/bin/env python
"""
fla.gr controller for view a list of current users
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.users.adminViewUsersTmpl import adminViewUsersTmpl

from models.user.userModel import userORM


@route("/admin/users")
class adminViewUsers(baseHTMLObject):
    __name__ = "admin users"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        view = adminViewUsersTmpl(searchList=[self.tmplSearchList])

        users = userORM.all()
        #Don't let you see people higher than you,
        #just out of safety for them...
        for user in users.rows:
            if user.level > self.session.level:
                users.rows.pop(users.rows.index(user))
        view.users = users

        return view
