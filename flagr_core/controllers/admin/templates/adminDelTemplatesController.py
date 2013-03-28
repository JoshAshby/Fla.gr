#!/usr/bin/env python
"""
fla.gr controller for deleting a template
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import config.dbBase as db
import models.template.templateModel as tm


@route("/admin/templates/(.*)/delete")
class adminDelTemplates(baseHTMLObject):
    __name__ = "admin templates"
    __level__ = 50
    __login__ = True
    def POST(self):
        tmplid = self.env["members"][0]

        tmpl = tm.templateORM.load(db.couchServer, tmplid)
        tmpl.delete()

        self.head = ("303 SEE OTHER", [("location", "/admin/templates")])
        self.session.pushAlert("We've deleted this template `%s`!"%tmpl.name, "Bye!", "warning")
