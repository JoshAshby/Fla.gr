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

from views.admin.users.adminNewUserTmpl import adminNewUserTmpl

import config.dbBase as db
from models.user.userModel import userORM


@route("/admin/users/new")
class adminUsers(baseHTMLObject):
    __name__ = "admin users"
    __level__ = 50
    def GET(self):
        """
        """
        id = self.env["members"][0]

        user = userORM.load(db.couchServer, id)
        view = adminNewUserTmpl(searchList=[self.tmplSearchList])

        view.editUser = user

        return view

    def POST(self):
        id = self.env["members"][0]
        password = self.env["members"]["password"] if self.env["members"].has_key("password") else None
        passwordTwice = self.env["members"]["passwordTwice"] if self.env["members"].has_key("passwordTwice") else None

        if password and passwordTwice:
            if password == passwordTwice:
                user = userORM.load(db.couchServer, id)
                user.setPassword(password)
                user.save()

                self.session.pushAlert("User `%s` updated" % user.username, "Yay", "success")

                self.head = ("303 SEE OTHER",
                    [("location", "/admin/users/%s/edit"%user.id)])

            else:
                view = adminNewUserTmpl(searchList=[self.tmplSearchList])
                view.passwordMatchError = True

                self.session.pushAlert("Those passwords don't match, please try again.", "", "error")

                return view
