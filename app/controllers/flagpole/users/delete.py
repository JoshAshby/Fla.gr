#!/usr/bin/env python
"""
fla.gr controller for deleting users

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
class delete(HTMLObject):
    def POST(self):
        userid = self.request.id

        if userid == self.request.session.userID:
            self.request.session.pushAlert("You can't delete yourself!",
                    "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/flagpole/users")])
            return

        user = userORM.find(userid)
        user.delete()

        self.request.session.pushAlert("User deleted...", level="success")
        self.head = ("302 FOUND",
            [("location", "/flagpole/users")])
