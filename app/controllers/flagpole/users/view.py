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

        user = userORM.find(userid)
        if not user:
            self.head = ("303 SEE OTHER", 
                [("location", "/flagpole/users")])
            self.request.session.pushAlert("That user couldn't be found!",
                "Oh no!", "error")

        self.view.data = {"user": user}
        return self.view
