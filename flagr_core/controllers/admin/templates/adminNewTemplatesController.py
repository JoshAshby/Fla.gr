#!/usr/bin/env python
"""
fla.gr controller for making a new template

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.templates.adminNewTemplatesTmpl import adminNewTemplatesTmpl

import models.template.templateModel as tm


@route("/admin/templates/new")
class adminNewTemplates(baseHTMLObject):
    __name__ = "admin templates"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        view = adminNewTemplatesTmpl(searchList=[self.tmplSearchList])
        return view

    def POST(self):
        name = self.env["members"]["name"] if self.env["members"].has_key("name") else ""
        description = self.env["members"]["description"] if self.env["members"].has_key("description") else ""
        template = self.env["members"]["template"] if self.env["members"].has_key("template") else ""

        if not name:
            view = adminNewTemplatesTmpl(searchList=[self.tmplSearchList])
            view.nameError = True

            view.description = description
            view.template = template

            return view

        tmpl = tm.templateORM(name=name, description=description, template=template)
        tmpl.save()

        self.head = ("303 SEE OTHER", [("location", "/admin/templates/%s"%tmpl.id)])
        self.session.pushAlert("We've created this template with the info you gave us!", "Congrats", "success")

