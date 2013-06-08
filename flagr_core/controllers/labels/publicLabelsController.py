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

from views.public.publicLabelsTmpl import publicLabelsTmpl

import models.couch.flag.flagModel as fm
import utils.labelUtils as lu


@autoRoute()
class labelsIndex(baseHTMLObject):
    _title = "public labels"
    def GET(self):
        """
        """
        if self.env["cfg"].enablePublicPages:
            view = publicLabelsTmpl(searchList=[self.tmplSearchList])

            flags = fm.flagORM.all()

            labels = lu.listLabels(flags, False)

            view.labels = labels

            return view
        else:
            self._404()
