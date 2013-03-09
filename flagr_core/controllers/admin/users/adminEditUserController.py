#!/usr/bin/env python
"""
fla.gr controller for editing users

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.users.adminEditUserTmpl import adminEditUserTmpl

import config.dbBase as db
from models.user.userModel import userORM


@route("/admin/users/(.*)/edit")
class adminEditUser(baseHTMLObject):
    __name__ = "admin users"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        userid = self.env["members"][0]

        user = userORM.load(db.couchServer, userid)
        view = adminEditUserTmpl(searchList=[self.tmplSearchList])

        view.editUser = user

        return view

    def POST(self):
        userid = self.env["members"][0]
        password = self.env["members"]["password"] if self.env["members"].has_key("password") else None
        passwordTwice = self.env["members"]["passwordTwice"] if self.env["members"].has_key("passwordTwice") else None
        about = self.env["members"]["about"] or ""
        level = self.env["members"]["level"] or 1
        email = self.env["members"]["email"] or ""
        emailVis = True if self.env["members"].has_key("emailVis") else False
        disable = True if self.env["members"].has_key("disable") else False

        user = userORM.load(db.couchServer, userid)
        user.about = about
        #Not allowed to edit your own level,
        #or disable to avoid down leveling or locking out on accident
        if self.session.id != userid:
            user.level = level
            user.disable = disable
        user.email = email
        user.emailVisibility = emailVis
        user.store(db.couchServer)

        if password and passwordTwice:
            if password == passwordTwice:
                user.setPassword(password)

            else:
                view = adminEditUserTmpl(searchList=[self.tmplSearchList])
                view.passwordMatchError = True

                self.session.pushAlert("Those passwords don't match, please try again.", "", "error")

                return view

        self.session.pushAlert("User `%s` updated" % user.username, "Yay", "success")

        self.head = ("303 SEE OTHER",
            [("location", "/admin/users")])
