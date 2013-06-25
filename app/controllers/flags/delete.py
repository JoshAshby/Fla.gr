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
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.flags.flagDelTmpl import flagDelTmpl

import models.couch.flag.flagModel as fm
import models.couch.flag.collections.userPublicFlagsCollection as pubfc
import models.couch.flag.collections.userFlagsCollection as fc

import utils.search.searchUtils as su


@autoRoute()
class flagsDelete(baseHTMLObject):
    _title = "delete flag"
    __login__ = True
    def GET(self):
        """
        """
        flagid = self.env["members"][0]

        flag = fm.flagORM.getByID(flagid)

        if flag.userID != self.session.id:
            self.session.pushAlert("You can't delete a flag you don't own!", "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/you/flags")])

            return

        view = flagDelTmpl(searchList=[self.tmplSearchList])

        view.flag = flag

        return view

    def POST(self):
        flagid = self.env["members"][0]

        flag = fm.flagORM.getByID(flagid)

        if flag.userID != self.session.id:
            self.session.pushAlert("You can't delete a flag you don't own!", "Can't do that!", "error")

            self.head = ("303 SEE OTHER",
                [("location", "/you/flags")])

            return

        pubFlags = pubfc.userPublicFlagsCollection(self.session.id)
        privFlags = fc.userFlagsCollection(self.session.id)
        if flag.visibility:
            pubFlags.delObject(flag.id)
        privFlags.delObject(flag.id)

        flag.delete()

        su.updateSearch()

        self.session.pushAlert("Flag `%s` deleted" % flag.title, "Bye!", "warning")

        self.head = ("303 SEE OTHER",
            [("location", "/you/flags")])
