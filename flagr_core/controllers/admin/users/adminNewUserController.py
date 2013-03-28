#!/usr/bin/env python
"""
fla.gr controller for making new users
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.users.adminNewUserTmpl import adminNewUserTmpl

from models.user.userModel import userORM


@route("/admin/users/new")
class adminNewUser(baseHTMLObject):
    __name__ = "admin users"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        view = adminNewUserTmpl(searchList=[self.tmplSearchList])

        return view

    def POST(self):
        name = self.env["members"]["username"]
        password = self.env["members"]["password"]
        passwordTwice = self.env["members"]["passwordTwice"]

        level = self.env["members"]["level"] or ""
        email = self.env["members"]["email"] or ""

        emailVis = True \
                if self.env["members"].has_key("emailVis") else False
        disable = True \
                if self.env["members"].has_key("disable") else False


        if password == passwordTwice \
                and password != "":
            try:
                newUser = userORM.new(name, password)

                newUser.level = level
                newUser.email = email
                newUser.emailVisibility = emailVis
                newUser.disable = disable
                newUser.save()

                self.session.pushAlert("New user with username `%s` \
                        created" % name, "Yay", "success")

                self.head = ("303 SEE OTHER",
                    [("location", str("/admin/users/%s/edit"%newUser.id))])
            except:
                view = adminNewUserTmpl(searchList=[self.tmplSearchList])
                view.usernameError = True

                self.session.pushAlert("You're going to have to pick a new \
                        username, `%s` is taken." % name, "", "error")

                return view

        else:
            view = adminNewUserTmpl(searchList=[self.tmplSearchList])
            view.passwordError = True

            self.session.pushAlert("Those passwords don't match, please \
                    try again.", "", "error")

            return view
