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

from views.public.publicFlagsTmpl import publicFlagsTmpl
from views.partials.flags.flagsListTmpl import flagsListTmpl

import models.couch.flag.flagModel as fm
import models.couch.baseCouchCollection as bcc

import utils.pagination as p


@autoRoute()
class flagsIndex(baseHTMLObject):
    _title = "public flags"
    def GET(self):
        """
        """
        if self.env["cfg"].enablePublicPages:
            page = self.env["members"]["p"] \
                    if self.env["members"].has_key("p") else 1

            view = publicFlagsTmpl(searchList=[self.tmplSearchList])

            flags = bcc.baseCouchCollection(fm.flagORM)
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

            return view
        else:
            self._404()
