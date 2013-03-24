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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.user.userFlagsTmpl import userFlagsTmpl

import models.flag.flagModel as fm
import models.user.userModel as um

import utils.pagination as p


@route("/user/(.*)/flags")
class userFlags(baseHTMLObject):
    __name__ = "flags"
    def GET(self):
        """
        """
        user = self.env["members"][0]
        page = self.env["members"]["p"] if self.env["members"].has_key("p") else 1

        view = userFlagsTmpl(searchList=[self.tmplSearchList])
        user = um.userORM.find(user)

        flags = fm.listFlagsByUserID(user.id)
        if flags:
            flags = fm.formatFlags(flags, False)

            for flag in flags:
                if not flag.visibility:
                    flags.pop(flags.index(flag))

        if self.env["cfg"].enableModalFlagDeletes:
            view.scripts = ["handlebars_1.0.min", "deleteFlagModal"]

        view.flags = p.pagination(flags, 10, int(page))
        view.flagAuthor = user

        return view
