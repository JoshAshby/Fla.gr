#!/usr/bin/env python
"""
fla.gr controller for deleting a template

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
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

        tmpl = tm.templateORM.load(db.couchServer,tmplid)
        db.couchServer.delete(tmpl)

        self.head = ("303 SEE OTHER", [("location", "/admin/templates")])
        self.session.pushAlert("We've deleted this template `%s`!"%tmpl.name, "Bye!", "warning")

