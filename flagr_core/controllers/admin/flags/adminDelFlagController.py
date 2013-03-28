#!/usr/bin/env python
"""
fla.gr controller for deleting flag
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.flags.adminDelFlagTmpl import adminDelFlagTmpl

import config.dbBase as db
from models.flag.flagModel import flagORM


@route("/admin/flags/(.*)/delete")
class adminDelFlag(baseHTMLObject):
    __name__ = "admin flags"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        flagid = self.env["members"][0]

        flag = flagORM.load(db.couchServer, flagid)
        view = adminDelFlagTmpl(searchList=[self.tmplSearchList])

        view.flag = flag

        return view

    def POST(self):
        flagid = self.env["members"][0]

        flag = flagORM.load(db.couchServer, flagid)
        flag.delete
        db.couchServer.delete(flag)

        self.session.pushAlert("Flag `%s` deleted" % flag.title, "Bye!", "warning")

        self.head = ("303 SEE OTHER",
            [("location", "/admin/flags")])
