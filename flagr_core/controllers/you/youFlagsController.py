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
import models.couch.flag.collections.userPublicFlagsCollection as pubfc
import models.couch.flag.collections.userPrivateFlagsCollection as privfc


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
                if self.env["members"].has_key("v") else "public"

        view = youFlagsTmpl(searchList=[self.tmplSearchList])

        if viewType == "public":
            flags = pubfc.userPublicFlagsCollection(self.session.id)
            flags.paginate(page, 25)
            flags.fetch()
            flags.format()

        elif viewType == "private":
            flags = privfc.userPrivateFlagsCollection(self.session.id)
            flags.paginate(page, 25)
            flags.fetch()
            flags.format()

        view.section = viewType

        if self.env["cfg"].enableModalFlagDeletes:
            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "adminModal.flagr",
                    "editForm.flagr",
                    "deleteFlagModal.flagr"]

        flagsTmpl = flagsListTmpl(searchList=[self.tmplSearchList])
        flagsTmpl.flags = flags

        view.flags = str(flagsTmpl)

        return view
