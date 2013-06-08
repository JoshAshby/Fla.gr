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
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.flags.flagViewTmpl import flagViewTmpl
from views.partials.flags.flagViewTmpl import flagViewTmpl as flagViewTmplPartial

import models.couch.flag.flagModel as fm


@autoRoute()
class flagsView(baseHTMLObject):
    _title = "view flag"
    def GET(self):
        """
        """
        flagid = self.env["members"][0]

        flag = fm.flagORM.getByID(flagid)
        if not flag.visibility and flag.userID != self.session.id:
            self.session.pushAlert("This is a private flag! Sorry but we \
                    can't let you see it.", "Hold it.", "error")
            self.head = ("303 SEE OTHER", [("location", "/flags")])
            return

        flag.format()

        view = flagViewTmpl(searchList=[self.tmplSearchList])

        if self.env["cfg"].enableModalFlagDeletes:
            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "adminModal.flagr",
                    "editForm.flagr",
                    "deleteFlagModal.flagr"]


        flagsTmpl = flagViewTmplPartial(searchList=[self.tmplSearchList])
        flagsTmpl.flag = flag

        view.flag = str(flagsTmpl)

        return view

