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

from views.admin.flags.adminEditFlagTmpl import adminEditFlagTmpl

from models.flag.flagModel import flagORM

import json


@route("/admin/flags/(.*)/edit")
class adminEditFlag(baseHTMLObject):
    __name__ = "admin flags"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        flagid = self.env["members"][0]

        flag = flagORM.getByID(flagid)
        view = adminEditFlagTmpl(searchList=[self.tmplSearchList])

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
            view.labels = flag.labels.join(", ")

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
            view = adminEditFlagTmpl(searchList=[self.tmplSearchList])

            view.titleError = True
            view.description = description
            view.labels = labels
            view.url = url
            view.id = flagid
            view.vis = visibility

            return view

        try:
            labels = list(set(json.loads(labels)))
        except:
            labels = list(set(labels.strip(" ").split(",")))

        flag = flagORM.getByID(flagid)
        flag.title = title
        flag.description = description
        flag.labels = labels
        flag.url = url
        flag.visibility = visibility

        flag.save()


        self.session.pushAlert("Flag `%s` updated" % flag.title, "Yay", "success")

        self.head = ("303 SEE OTHER",
            [("location", "/admin/flags")])
