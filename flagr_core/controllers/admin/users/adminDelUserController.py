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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.users.adminDelUserTmpl import adminDelUserTmpl

import config.dbBase as db
from models.user.userModel import userORM


@route("/admin/users/(.*)/delete")
class adminDelUser(baseHTMLObject):
    __name__ = "admin users"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        userid = self.env["members"][0]

        if userid == self.session.id:
            self.session.pushAlert("You can't delete yourself!",
                    "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/admin/users")])

            return

        user = userORM.load(db.couchServer, userid)
        view = adminDelUserTmpl(searchList=[self.tmplSearchList])

        view.editUser = user

        return view

    def POST(self):
        userid = self.env["members"][0]

        if userid == self.session.id:
            self.session.pushAlert("You can't delete yourself!",
                    "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/admin/users")])

            return

        user = userORM.load(db.couchServer, userid)
        user.delete()

        self.session.pushAlert("User `%s` deleted" % user.username,
                "Bye!", "success")

        self.head = ("303 SEE OTHER",
            [("location", "/admin/users")])
