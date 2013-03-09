#!/usr/bin/env python
"""
fla.gr controller for deleting flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.flags.flagDelTmpl import flagDelTmpl

import config.dbBase as db
import models.flag.flagModel as fm


@route("/flags/(.*)/delete")
class adminDelUser(baseHTMLObject):
    __name__ = "delete flag"
    __login__ = True
    def GET(self):
        """
        """
        flagid = self.env["members"][0]

        flag = fm.flagORM.load(db.couchServer, flagid)

        if flag.userID != self.session.id:
            self.session.pushAlert("You can't delete a flag you don't own!", "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/your/flags")])

            return

        view = flagDelTmpl(searchList=[self.tmplSearchList])

        view.flag = flag

        return view

    def POST(self):
        flagid = self.env["members"][0]

        flag = fm.flagORM.load(db.couchServer, flagid)

        if flag.userID != self.session.id:
            self.session.pushAlert("You can't delete a flag you don't own!", "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/your/flags")])

            return

        db.couchServer.delete(flag)

        self.session.pushAlert("Flag `%s` deleted" % flag.title, "Bye!", "warning")

        self.head = ("303 SEE OTHER",
            [("location", "/your/flags")])
