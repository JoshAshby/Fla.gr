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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.public.publicFlagsTmpl import publicFlagsTmpl

import config.dbBase as db
from models.user.userModel import userORM
import models.flag.flagModel as fm

import utils.pagination as p


@route("/flags")
@route("/public/flags")
class publicFlags(baseHTMLObject):
    __name__ = "public flags"
    def GET(self):
        """
        """
        page = self.env["members"]["p"] if self.env["members"].has_key("p") else 1
        view = publicFlagsTmpl(searchList=[self.tmplSearchList])

        flags = list(fm.flagORM.view(db.couchServer, 'typeViews/flag'))
        flags = fm.formatFlags(flags, False)

        for flag in flags:
            flag.author = userORM.load(db.couchServer, flag.userID)

        if self.env["cfg"].enableModalFlagDeletes:
            view.scripts = ["handlebars_1.0.min",
                    "deleteFlagModal.flagr"]

        view.flags = p.pagination(flags, 10, int(page))

        return view
