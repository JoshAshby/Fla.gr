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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.flags.flagEditTmpl import flagEditTmpl

import models.flag.flagModel as fm
from datetime import datetime
import config.dbBase as db
import json


@route("/flags/(.*)/edit")
class flagEdit(baseHTMLObject):
    __name__ = "edit flag"
    def GET(self):
        """
        """
        flagid = self.env["members"][0]
        view = flagEditTmpl(searchList=[self.tmplSearchList])

        flag = fm.flagORM.load(db.couchServer, flagid)

        view.title = flag.title
        view.description = flag.description
        try:
            view.labels = json.dumps(flag.labels)
        except:
            view.labels = ""
        view.url = flag.url

        if self.env["cfg"].enableDynamicLabels:
            view.scripts = ["handlebars_1.0.min", "jquery.json-2.4.min", "dynamicLabels"]

        return view

    def POST(self):
        flagid = self.env["members"][0]
        title = self.env["members"]["title"] if self.env["members"].has_key("title") else None
        description = self.env["members"]["description"] or ""
        labels = self.env["members"]["labels"] or ""
        url = self.env["members"]["url"] or ""
        visibility = True if self.env["members"].has_key("vis") and self.env["members"]["vis"] == "on" else False

        if not title:
            self.session.pushAlert("We can't make a flag with no title!", "Whoa there kiddo...", "error")
            view = flagEditTmpl(searchList=[self.tmplSearchList])

            view.titleError = True
            view.description = description
            view.labels = labels
            view.url = url

            return view

        try:
            labels = json.loads(labels)
        except:
            labels = ""

        flag = fm.flagORM.load(db.couchServer, flagid)
        flag.title = title
        flag.description = description
        flag.labels = labels
        flag.url = url
        flag.visibility = visibility
        flag.created = datetime.now()

        flag.save()

        self.session.pushAlert("The flag `%s` has been updated"%flag.title, "Yay!", "success")

        self.head = ("303 SEE OTHER",
            [("location", str("/flags/%s"%flag.id))])
