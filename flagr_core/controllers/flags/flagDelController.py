#!/usr/bin/env python
"""
fla.gr controller for deleting flags
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.flags.flagDelTmpl import flagDelTmpl

import config.dbBase as db
import models.flag.flagModel as fm

import utils.search.searchUtils as su


@route("/flags/(.*)/delete")
class flagDel(baseHTMLObject):
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

        flag.delete()

        su.updateSearch()

        self.session.pushAlert("Flag `%s` deleted" % flag.title, "Bye!", "warning")

        self.head = ("303 SEE OTHER",
            [("location", "/your/flags")])
