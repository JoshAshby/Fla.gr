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
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import *

from models.couch.user.userModel import userORM


@autoRoute()
@admin()
class edit(HTMLObject):
    _title = "admin users"
    def POST(self):
        userid = self.request.id
        password = self.request.getParam("password")
        passwordTwice = self.request.getParam("passwordTwice")
        about = self.request.getParam("about")
        level = self.request.getParam("level", 1)
        email = self.request.getParam("emailVis", False)
        disable = self.request.getParam("disable", False)

        user = userORM.getByID(userid)
        user.about = about
        #Not allowed to edit your own level,
        #or disable to avoid down leveling or locking out on accident
        if self.request.session.userID != userid:
            user.level = level
            user.disable = disable
        user.email = email
        user.emailVisibility = emailVis
        user.save()

        if password and passwordTwice:
            if password == passwordTwice:
                user.setPassword(password)

            else:
                pass

        self.request.session.pushAlert("User %s was update!" % user.username, "Yay!", "success")

        self.head = ("200 OK",
            [("location", "/flagpole/users/view/%s" % userid)])
