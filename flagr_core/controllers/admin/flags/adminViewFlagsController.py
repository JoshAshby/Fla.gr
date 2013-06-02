#!/usr/bin/env python
"""
fla.gr controller for view a list of current flags and status

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.admin.flags.adminViewFlagsTmpl import adminViewFlagsTmpl

from models.couch.user.userModel import userORM
import models.couch.flag.flagModel as fm


@autoRoute()
class adminFlagsIndex(baseHTMLObject):
    _title = "admin flags"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        view = adminViewFlagsTmpl(searchList=[self.tmplSearchList])

        flags = fm.flagORM.all()
        flags = fm.formatFlags(flags, True)

        for flag in flags:
            flag.author = userORM.getByID(flag.userID)

        view.flags = flags

        return view
