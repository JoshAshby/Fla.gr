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
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.admin.templates.adminNewTemplatesTmpl import adminNewTemplatesTmpl

import models.template.templateModel as tm
import models.setting.settingModel as sm


@autoRoute()
class adminTemplatesNew(baseHTMLObject):
    _title = "admin templates"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        view = adminNewTemplatesTmpl(searchList=[self.tmplSearchList])

        try:
            currentTypes = sm.getSetting("templates", "types")
        except:
            currentTypes = {"Set template types in settings"}

        view.templateTypes = currentTypes

        return view

    def POST(self):
        name = self.env["members"]["name"] if self.env["members"].has_key("name") else ""
        description = self.env["members"]["description"] if self.env["members"].has_key("description") else ""
        template = self.env["members"]["template"] if self.env["members"].has_key("template") else ""
        tmplType = self.env["members"]["type"] if self.env["members"].has_key("type") else ""

        if not name:
            view = adminNewTemplatesTmpl(searchList=[self.tmplSearchList])
            view.nameError = True

            view.description = description
            view.template = template

            try:
                currentTypes = sm.getSetting("templates", "types")
            except:
                currentTypes = {"Set template types in settings"}

            view.templateTypes = currentTypes

            return view

        tmpl = tm.templateORM(name=name, description=description, template=template, type=tmplType)
        tmpl.save()

        self.head = ("303 SEE OTHER", [("location", "/admin/templates/view/%s"%tmpl.id)])
        self.session.pushAlert("We've created this template with the info you gave us!", "Congrats", "success")

