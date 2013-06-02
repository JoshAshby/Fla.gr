#!/usr/bin/env python
"""
fla.gr controller for viewing the logged in users flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute, route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youFlagsTmpl import youFlagsTmpl
from views.partials.flags.flagsListTmpl import flagsListTmpl

import models.couch.flag.flagModel as fm

import utils.pagination as p


@route("/your/flags")
@autoRoute()
class youFlags(baseHTMLObject):
    _title = "flags"
    __login__ = True
    def GET(self):
        """
        """
        page = self.env["members"]["p"] \
                if self.env["members"].has_key("p") else 1

        viewType = self.env["members"]["v"] \
                if self.env["members"].has_key("v") else ""

        view = youFlagsTmpl(searchList=[self.tmplSearchList])

        flags = fm.listFlagsByUserID(self.session.id)
        if flags:
            if viewType == "public":
                flags = fm.formatFlags(flags, False)
                view.section = "public"
            elif viewType == "private":
                flags = fm.formatFlags(flags, True)
                tmpFlags = []
                for flag in flags:
                    if not flag.visibility:
                        tmpFlags.append(flag)
                flags = tmpFlags
                view.section = "private"
            else:
                flags = fm.formatFlags(flags, True)
                view.section = "all"

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

        return view
