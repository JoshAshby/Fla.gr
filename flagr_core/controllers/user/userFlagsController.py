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

import models.couch.flag.flagModel as fm
import models.couch.user.userModel as um
import models.couch.flag.collections.userPublicFlagsCollection as pubfc


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

        flags = pubfc.userPublicFlagsCollection(user.id)
        flags.paginate(page, 25)
        flags.fetch()
        flags.format()

        if self.env["cfg"].enableModalFlagDeletes:
            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "adminModal.flagr",
                    "editForm.flagr",
                    "deleteFlagModal.flagr"]

        flagsTmpl = flagsListTmpl(searchList=[self.tmplSearchList])
        flagsTmpl.flags = flags

        view.flags = str(flagsTmpl)
        view.author = user

        return view
