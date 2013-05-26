#!/usr/bin/env python
"""
fla.gr controller for deleting lots of templates

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import models.template.templateModel as tm

import json


@route("/admin/templates/delete")
class adminBulkDelTemplates(baseHTMLObject):
    _title = "admin templates"
    __level__ = 50
    __login__ = True
    def POST(self):
        tmplids = json.loads(self.env["members"]["array"]) if self.env["members"].has_key("array") else []

        for ID in tmplids:
            tmpl = tm.templateORM.getByID(ID)
            tmpl.delete()

        self.head = ("303 SEE OTHER", [("location", "/admin/templates")])
        self.session.pushAlert("You've deleted all of those templates. Hope they weren't being used anywhere!", "Bye!", "success")
