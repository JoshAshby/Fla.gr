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
from seshat.baseObject import HTMLObject
from seshat.objectMods import *

from models.couch.flag.flagModel import flagORM
import models.couch.flag.collections.userPublicFlagsCollection as pubfc
import models.couch.flag.collections.userFlagsCollection as fc


@autoRoute()
@admin()
class delete(HTMLObject):
    _title = "admin flags"
    def POST(self):
        flagid = self.request.id

        flag = flagORM.getByID(flagid)
        pubFlags = pubfc.userPublicFlagsCollection(flag.userID)
        privFlags = fc.userFlagsCollection(flag.userID)
        if flag.visibility:
            pubFlags.delObject(flag.id)
        privFlags.delObject(flag.id)

        flag.delete()

        self.request.session.pushAlert("Flag `%s` deleted" % flag.title, "Bye!", "success")

        self.head = ("303 SEE OTHER",
            [("location", "/flagpole/flags")])
