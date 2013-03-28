#!/usr/bin/env python
"""
fla.gr controller for deleting lots of templates
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import config.dbBase as db
import models.template.templateModel as tm
import json


@route("/admin/templates/delete")
class adminBulkDelTemplates(baseHTMLObject):
    __name__ = "admin templates"
    __level__ = 50
    __login__ = True
    def POST(self):
        tmplids = json.loads(self.env["members"]["array"]) if self.env["members"].has_key("array") else []

        for ID in tmplids:
            tmpl = tm.templateORM.load(db.couchServer, ID)
            tmpl.delete()

        self.head = ("303 SEE OTHER", [("location", "/admin/templates")])
        self.session.pushAlert("You've deleted all of those templates. Hope they weren't being used anywhere!", "Bye!", "success")
