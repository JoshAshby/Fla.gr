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
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import *

from models.couch.user.userModel import userORM


@autoRoute()
@admin()
class new(HTMLObject):
    _title = "admin users"
    _defaultTmpl = "flagpole/users/new"
    def GET(self):
        """
        """
        return self.view

    def POST(self):
        name = self.request.getParam("username")
        password = self.request.getParam("password")
        passwordTwice = self.request.getParam("passwordTwice")

        level = self.request.getParam("level")
        email = self.request.getParam("email")
        emailVis = self.request.getParam("emailVis", False)
        disable = self.request.getParam("disable", False)

        level = self.env["members"]["level"] or ""
        email = self.env["members"]["email"] or ""


        if password and password == passwordTwice:
            try:
                newUser = userORM.new(name, password)

                newUser.level = level
                newUser.email = email
                newUser.emailVisibility = emailVis
                newUser.disable = disable
                newUser.save()

                self.request.session.pushAlert("New user with username `%s` \
                        created" % name, "Yay", "success")

                self.head = ("200 OK",
                    [("location", str("/flagpole/users/view/%s"%newUser.id))])

            except userError:

                self.request.session.pushAlert("You're going to have to pick a new \
                        username, `%s` is taken." % name, "", "error")

                self.view.data = {"usernameError": True}
                return self.view

        else:
            self.request.session.pushAlert("Those passwords don't match, please \
                    try again.", "", "error")

            self.view.data = {"passwordError": True}
            return self.view
