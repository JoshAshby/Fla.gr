#!/usr/bin/env python
"""
fla.gr controller for viewing the logged in users labels
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youLabelsTmpl import youLabelsTmpl

import models.flag.flagModel as fm
import utils.labelUtils as lu


@route("/your/labels")
class youLabels(baseHTMLObject):
    __name__ = "labels"
    __login__ = True
    def GET(self):
        """
        """
        view = youLabelsTmpl(searchList=[self.tmplSearchList])

        flags = fm.listFlagsByUserID(self.session.id)
        if flags:
            labels = lu.listLabels(flags, True)

        view.labels = labels

        return view
