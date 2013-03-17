#!/usr/bin/env python
"""
fla.gr controller for editing a template

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.templates.adminEditTemplatesTmpl import adminEditTemplatesTmpl

import config.dbBase as db
import models.template.templateModel as tm
from datetime import datetime


@route("/admin/templates/(.*)/edit")
class adminEditTemplates(baseHTMLObject):
    __name__ = "admin templates"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        tmplid = self.env["members"][0]
        view = adminEditTemplatesTmpl(searchList=[self.tmplSearchList])

        template = tm.templateORM.load(db.couchServer,tmplid)

        view.tmpl = template

        return view

    def POST(self):
        name = self.env["members"]["name"] if self.env["members"].has_key("name") else ""
        description = self.env["members"]["description"] if self.env["members"].has_key("description") else ""
        template = self.env["members"]["template"] if self.env["members"].has_key("template") else ""
        tmplid = self.env["members"][0]

        tmpl = tm.templateORM.load(db.couchServer,tmplid)
        tmpl.description = description
        tmpl.template = template

        if not name:
            view = adminEditTemplatesTmpl(searchList=[self.tmplSearchList])
            view.nameError = True

            view.tmpl = tmpl

            return view

        tmpl.name = name
        tmpl.created = datetime.now()

        tmpl.save()

        self.head = ("303 SEE OTHER", [("location", "/admin/templates/%s"%tmplid)])
        self.session.pushAlert("We've updated this template!", "Congrats", "success")

