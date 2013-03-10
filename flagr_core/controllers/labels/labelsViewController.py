#!/usr/bin/env python
"""
fla.gr controller for viewing the logged in users labels

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.labels.labelsViewTmpl import labelsViewTmpl

import models.flag.flagModel as fm
import re


@route("/labels/(.*)")
class labelsView(baseHTMLObject):
    __name__ = "labels"
    __login__ = True
    def GET(self):
        """
        """
        baseLabel = self.env["members"][0]
        view = labelsViewTmpl(searchList=[self.tmplSearchList])
        labelRe = re.compile(baseLabel+'(.*)')

        matchedFlags = []
        labels = []
        flags = fm.listFlagsByUserID(self.session.id)
        for flag in flags:
            for label in flag.labels:
                if labelRe.match(label):
                    labels.append(label)
                    matchedFlags.append(flag)

        if baseLabel in labels:
            labels.pop(labels.index(baseLabel))

        view.labels = labels
        view.baseLabel = baseLabel
        view.flags = fm.formateFlags(matchedFlags)

        return view
