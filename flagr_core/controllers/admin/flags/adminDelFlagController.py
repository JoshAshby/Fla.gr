#!/usr/bin/env python
"""
fla.gr controller for deleting flag

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.admin.flags.adminDelFlagTmpl import adminDelFlagTmpl

from models.couch.flag.flagModel import flagORM
import models.couch.flag.collections.userPublicFlagsCollection as pubfc
import models.couch.flag.collections.userPrivateFlagsCollection as privfc


@autoRoute()
class adminFlagsDelete(baseHTMLObject):
    _title = "admin flags"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        flagid = self.env["members"][0]

        flag = flagORM.getByID(flagid)
        view = adminDelFlagTmpl(searchList=[self.tmplSearchList])

        view.flag = flag

        return view

    def POST(self):
        flagid = self.env["members"][0]

        flag = flagORM.getByID(flagid)
        pubFlags = pubfc.userPublicFlagsCollection(flag.userID)
        privFlags = privfc.userPrivateFlagsCollection(flag.userID)
        if flag.visibility:
            pubFlags.delObject(flag.id)
        else:
            privFlags.delObject(flag.id)

        flag.delete()

        self.session.pushAlert("Flag `%s` deleted" % flag.title, "Bye!", "warning")

        self.head = ("303 SEE OTHER",
            [("location", "/admin/flags")])
