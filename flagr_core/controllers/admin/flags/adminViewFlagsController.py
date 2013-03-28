#!/usr/bin/env python
"""
fla.gr controller for view a list of current flags and status
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.flags.adminViewFlagsTmpl import adminViewFlagsTmpl

from models.user.userModel import userORM
import models.flag.flagModel as fm


@route("/admin/flags")
class adminViewFlags(baseHTMLObject):
    __name__ = "admin flags"
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
