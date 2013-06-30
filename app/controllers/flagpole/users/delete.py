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
from seshat.baseObject import JSONObject
from seshat.objectMods import *

from models.couch.user.userModel import userORM


@autoRoute()
@admin()
class delete(JSONObject):
    def GET(self):
        raise Exception("test")

    def POST(self):
        userid = self.request.id

        if userid == self.request.session.userID:
            self.request.session.pushAlert("You can't delete yourself!",
                    "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/flagpole/users")])

            return

        error = ""
        status = False
        try:
            user = userORM.getByID(userid)
            user.delete()
            status = True
        except Exception as e:
            error = str(e)

        return {"user": user.id, "action": "delete", "success": status}
