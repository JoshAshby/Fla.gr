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

from views.flags.flagEditTmpl import flagEditTmpl

import models.flag.flagModel as fm
import utils.markdownUtils as mdu

from datetime import datetime
import json

import utils.search.searchUtils as su


@autoRoute()
class flagsEdit(baseHTMLObject):
    _title = "edit flag"
    __login__ = True
    def GET(self):
        """
        """
        flagid = self.env["members"][0]
        flag = fm.flagORM.getByID(flagid)

        if flag.userID != self.session.id:
            self.head = ("303 SEE OTHER", [("Location", "/flags/view/%s"%flagid)])
            self.session.pushAlert("You can't edit someone else's flag! We're working on a cloning feature but until then, just hold tight or copy and paste the flag.", "Hold it!", "error")

            return

        view = flagEditTmpl(searchList=[self.tmplSearchList])
        view.id = flagid

        view.title = flag.title
        view.description = flag.description
        view.url = flag.url
        view.vis = flag.visibility

        if self.env["cfg"].enableDynamicLabels:
            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "dynamicInput.flagr"]
            view.labels = json.dumps(flag.labels)
        else:
            view.labels = ", ".join(flag.labels).strip(", ")

        return view

    def POST(self):
        flagid = self.env["members"][0]
        title = self.env["members"]["title"] if self.env["members"].has_key("title") else None
        description = self.env["members"]["description"] or ""
        labels = self.env["members"]["labels"] or ""
        url = self.env["members"]["url"] or ""
        visibility = True if self.env["members"].has_key("vis") and self.env["members"]["vis"] == "on" else False

        flag = fm.flagORM.getByID(flagid)

        if flag.userID != self.session.id:
            self.head = ("303 SEE OTHER", [("Location", "/flags/view/%s"%flagid)])
            self.session.pushAlert("You can't edit someone else's flag! We're working on a cloning feature but until then, just hold tight or copy and paste the flag.", "Hold it!", "error")

            return

        if not title:
            self.session.pushAlert("We can't make a flag with no title!", "Whoa there kiddo...", "error")
            view = flagEditTmpl(searchList=[self.tmplSearchList])

            view.titleError = True
            view.description = description
            view.labels = labels
            view.url = url
            view.id = flagid
            view.vis = visibility

            return view

        #Will only work if self.env["cfg"].enableDynamicLabels is enabled
        #otherwise it will fall over to the except
        try:
            labels = list(set(json.loads(labels)))
        except:
            labels = list(set(labels.replace(" ", "").split(",")))

        for label in range(len(labels)):
            labels[label] = mdu.cleanInput(labels[label])

        flag.title = mdu.cleanInput(title)
        flag.description = description
        flag.labels = labels
        flag.url = url
        flag.visibility = visibility
        flag.created = datetime.now()

        flag.save()

        su.updateSearch()

        self.session.pushAlert("The flag `%s` has been updated"%flag.title, "Yay!", "success")

        self.head = ("303 SEE OTHER",
            [("location", str("/flags/view/%s"%flag.id))])
