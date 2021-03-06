#!/usr/bin/env python
"""
fla.gr controller for making new flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.flags.flagNewTmpl import flagNewTmpl

import models.couch.flag.flagModel as fm
import models.couch.flag.collections.userPublicFlagsCollection as pubfc
import models.couch.flag.collections.userFlagsCollection as fc
import json
import utils.markdownUtils as mdu

import utils.search.searchUtils as su


@autoRoute()
class flagsNew(baseHTMLObject):
    _title = "new flag"
    __login__ = True
    def GET(self):
        """
        """
        view = flagNewTmpl(searchList=[self.tmplSearchList])

        if self.env["cfg"].enableDynamicLabels:
            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "dynamicInput.flagr"]

        return view

    def POST(self):
        title = self.env["members"]["title"] if self.env["members"].has_key("title") else None
        description = self.env["members"]["description"] or ""
        labels = self.env["members"]["labels"] if self.env["members"].has_key("labels") else ""
        url = self.env["members"]["url"] if self.env["members"].has_key("url") else ""
        visibility = True if self.env["members"].has_key("vis") and self.env["members"]["vis"] == "on" else False

        if not title:
            self.session.pushAlert("We can't make a flag with no title!", "Whoa there kiddo...", "error")
            view = flagNewTmpl(searchList=[self.tmplSearchList])

            view.titleError = True
            view.description = description
            view.labels = labels
            view.url = url
            view.vis = visibility

            return view

        try:
            labels = list(set(json.loads(labels)))
        except:
            labels = list(set(labels.strip(" ").split(",")))

        for label in range(len(labels)):
            labels[label] = mdu.cleanInput(labels[label])

        newFlag = fm.flagORM(title=mdu.cleanInput(title), description=description, labels=labels, url=url, userID=self.session.id, visibility=visibility)

        pubFlags = pubfc.userPublicFlagsCollection(self.session.id)
        privFlags = fc.userFlagsCollection(self.session.id)
        if visibility:
            pubFlags.addObject(newFlag.id)
        privFlags.addObject(newFlag.id)

        newFlag.save()

        su.updateSearch()

        self.session.pushAlert("Hey look, you've made another flag!", "Horay!", "success")

        self.head = ("303 SEE OTHER",
            [("location", str("/flags/view/%s"%newFlag.id))])
