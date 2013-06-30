#!/usr/bin/env python
"""
fla.gr controller to view an individual user

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
class view(HTMLObject):
    _title = "flagpole user"
    _defaultTmpl = "flagpole/users/singleUser"
    def GET(self):
        """
        """
        userid = self.request.id
        if not userid:
            self.head = ("303 SEE OTHER",
                [("location", "/flagpole/users")])
            return

        user = userORM.find(userid)
        if not user:
            self.head = ("303 SEE OTHER", 
                [("location", "/flagpole/users")])
            self.request.session.pushAlert("That user couldn't be found!",
                "Oh no!", "error")
            return

        user.format()

        self.view.scripts = ["handlebars_1.0.min",
            "modal.flagr",
            "flagpole/user.flagr"]
        self.view.data = {"user": user}
        return self.view

    def POST(self):
        userid = self.request.id
        password = self.request.getParam("password")
        passwordTwice = self.request.getParam("passwordTwice")
        email = self.request.getParam("email")
        about = self.request.getParam("about")
        level = self.request.getParam("level", 1)
        emailVis = self.request.getParam("emailVis", False)
        disable = self.request.getParam("disable", False)

        user = userORM.find(userid)

        if password and passwordTwice:
            if password == passwordTwice:
                user.setPassword(password)

            else:
              self.view.data = {"passwordError": True}
              return self.view
        else:
            user.about = about
            #Not allowed to edit your own level,
            #or disable to avoid down leveling or locking out on accident
            if self.request.session.userID != userid:
                if level: user.level = level

            user.email = email
            user.emailVisibility = emailVis
            user.disable = disable
            user.save()

        if not disable:
            self.request.session.pushAlert("User updated!", "Yay!", "success")
        else:
            self.request.session.pushAlert("User disabled :/", "Welp...", "success")

        self.head = ("302 FOUND",
            [("location", "/flagpole/users/view/"+str(user.id))])
