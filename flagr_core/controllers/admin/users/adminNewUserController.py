#!/usr/bin/env python
"""
fla.gr controller for making new users

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

from models.user.userModel import userORM


@route("/admin/users/new")
class adminUsers(baseHTMLObject):
    __name__ = "admin users"
    __level__ = 50
    def GET(self):
        """
        """
        view = adminNewUserTmpl(searchList=[self.tmplSearchList])

        return view

    def POST(self):
        name = self.env["members"]["username"]
        password = self.env["members"]["password"]
        passwordTwice = self.env["members"]["passwordTwice"]

        if password == passwordTwice:
            try:
                newUser = userORM.new(name, password)
                newUser.save()

                self.session.pushAlert("New user with username `%s` created" % name, "Yay", "success")

                self.head = ("303 SEE OTHER",
                    [("location", "/admin/users/%s/edit"%newUser.id)])
            except:
                view = adminNewUserTmpl(searchList=[self.tmplSearchList])
                view.usernameError = True

                self.session.pushAlert("You're going to have to pick a new username, `%s` is taken." % name, "", "error")

                return view

        else:
            view = adminNewUserTmpl(searchList=[self.tmplSearchList])
            view.passwordError = True

            self.session.pushAlert("Those passwords don't match, please try again.", "", "error")

            return view
