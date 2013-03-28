#!/usr/bin/env python
"""
fla.gr controller for view a list of current flags and status
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.public.publicLabelsTmpl import publicLabelsTmpl

import models.flag.flagModel as fm
import utils.labelUtils as lu


@route("/labels")
@route("/public/labels")
class publicLabels(baseHTMLObject):
    __name__ = "public labels"
    def GET(self):
        """
        """
        view = publicLabelsTmpl(searchList=[self.tmplSearchList])

        flags = fm.flagORM.all()

        labels = lu.listLabels(flags, False)

        view.labels = labels

        return view
