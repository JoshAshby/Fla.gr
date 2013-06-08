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
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.labels.labelsViewTmpl import labelsViewTmpl
from views.partials.flags.flagsListTmpl import flagsListTmpl

import models.couch.flag.flagModel as fm
import re


#@autoRoute()
class labelsView(baseHTMLObject):
    _title = "labels"
    __login__ = True
    def GET(self):
        """
        """
        if self.env["cfg"].enablePublicPages:
            page = self.env["members"]["p"] \
                    if self.env["members"].has_key("p") else 1
            baseLabel = self.env["members"][0]

            if type(baseLabel) == list:
                baseLabel = "/".join(baseLabel)

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

            if self.env["cfg"].enableModalFlagDeletes:
                view.scripts = ["handlebars_1.0.min",
                        "jquery.json-2.4.min",
                        "adminModal.flagr",
                        "editForm.flagr",
                        "deleteFlagModal.flagr"]

            flags = fm.formatFlags(matchedFlags, False)

            flagsTmpl = flagsListTmpl(searchList=[self.tmplSearchList])
            flagsTmpl.flags = flags

            view.flags = str(flagsTmpl)

            view.labels = labels
            view.baseLabel = baseLabel

            return view
        else:
            self._404()
