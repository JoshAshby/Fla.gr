#!/usr/bin/env python
"""
fla.gr controller for viewing a given users public flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.user.userFlagsTmpl import userFlagsTmpl
from views.partials.flags.flagsListTmpl import flagsListTmpl

import models.flag.flagModel as fm
import models.user.userModel as um

import utils.pagination as p


@autoRoute()
class userFlags(baseHTMLObject):
    _title = "flags"
    def GET(self):
        """
        """
        user = self.env["members"][0]
        page = self.env["members"]["p"] \
                if self.env["members"].has_key("p") else 1

        view = userFlagsTmpl(searchList=[self.tmplSearchList])
        user = um.userORM.find(user)

        flags = fm.listFlagsByUserID(user.id)
        if flags:
            flags = fm.formatFlags(flags, False)

            for flag in flags:
                if not flag.visibility:
                    flags.pop(flags.index(flag))

        if self.env["cfg"].enableModalFlagDeletes:
            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "adminModal.flagr",
                    "editForm.flagr",
                    "deleteFlagModal.flagr"]

        flags = p.pagination(flags, 10, int(page))

        flagsTmpl = flagsListTmpl(searchList=[self.tmplSearchList])
        flagsTmpl.flags = flags

        view.flags = str(flagsTmpl)
        view.author = user

        return view
