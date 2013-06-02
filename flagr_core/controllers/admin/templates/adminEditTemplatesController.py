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
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.admin.templates.adminEditTemplatesTmpl import adminEditTemplatesTmpl

import models.couch.template.templateModel as tm
import models.redis.setting.settingModel as sm

from datetime import datetime


@autoRoute()
class adminTemplatesEdit(baseHTMLObject):
    _title = "admin templates"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        tmplid = self.env["members"][0]
        view = adminEditTemplatesTmpl(searchList=[self.tmplSearchList])

        template = tm.templateORM.getByID(tmplid)

        try:
            currentTypes = sm.getSetting("templates", "types")
        except:
            currentTypes = {"Set template types in settings"}

        view.templateTypes = currentTypes
        view.tmpl = template

        return view

    def POST(self):
        name = self.env["members"]["name"] if self.env["members"].has_key("name") else ""
        description = self.env["members"]["description"] if self.env["members"].has_key("description") else ""
        template = self.env["members"]["template"] if self.env["members"].has_key("template") else ""
        tmplType = self.env["members"]["type"] if self.env["members"].has_key("type") else ""

        tmplid = self.env["members"][0]


        tmpl = tm.templateORM.getByID(tmplid)
        tmpl.description = description
        tmpl.template = template
        tmpl.type = tmplType

        if not name:
            try:
                currentTypes = sm.getSetting("templates", "types")
            except:
                currentTypes = {"Set template types in settings"}

            view = adminEditTemplatesTmpl(searchList=[self.tmplSearchList])
            view.nameError = True

            view.templateTypes = currentTypes
            view.tmpl = tmpl

            return view

        tmpl.name = name
        tmpl.created = datetime.now()

        tmpl.save()

        self.head = ("303 SEE OTHER", [("location", "/admin/templates/view/%s"%tmplid)])
        self.session.pushAlert("We've updated this template!", "Congrats", "success")

