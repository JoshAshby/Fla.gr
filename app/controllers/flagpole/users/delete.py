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
from seshat.baseHTMLObject import baseHTMLObject
from seshat.objectMods import *

from models.couch.user.userModel import userORM


@autoRoute()
@admin()
class delete(baseHTMLObject):
    _title = "admin users"
    def POST(self):
        userid = self.request.id

        if userid == self.request.session.userID:
            self.request.session.pushAlert("You can't delete yourself!",
                    "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/flagpole/users")])

            return

        user = userORM.getByID(userid)
        user.delete()

        self.request.session.pushAlert("User `%s` deleted" % user.username,
                "Bye!", "success")

        self.head = ("200 OK",
            [("location", "/flagpole/users")])
