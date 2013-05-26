#!/usr/bin/env python
"""
fla.gr controller for editing flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.flags.flagViewTmpl import flagViewTmpl
from views.partials.flags.flagsListTmpl import flagsListTmpl

import models.flag.flagModel as fm
import utils.pagination as p

@route("/flags/(.*)")
class flagView(baseHTMLObject):
    _title = "view flag"
    def GET(self):
        """
        """
        flagid = self.env["members"][0]
        page = self.env["members"]["p"] \
                if self.env["members"].has_key("p") else 1

        flag = fm.flagORM.getByID(flagid)
        if not flag.visibility and flag.userID != self.session.id:
            self.session.pushAlert("This is a private flag! Sorry but we \
                    can't let you see it.", "Hold it.", "error")
            self.head = ("303 SEE OTHER", [("location", "/flags")])
            return

        view = flagViewTmpl(searchList=[self.tmplSearchList])

        flag = fm.formatFlag(flag)

        view.flag = flag

        if self.env["cfg"].enableModalFlagDeletes:
            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "adminModal.flagr",
                    "editForm.flagr",
                    "deleteFlagModal.flagr"]

        flag = fm.formatFlag(flag)
        flag = p.pagination([flag], 10, int(page))

        flagsTmpl = flagsListTmpl(searchList=[self.tmplSearchList])
        flagsTmpl.flags = flag

        view.flags = str(flagsTmpl)

        return view

