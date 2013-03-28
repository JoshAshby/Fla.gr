#!/usr/bin/env python
"""
fla.gr controller for view a list of current templates
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.templates.adminInfoTemplatesTmpl import adminInfoTemplatesTmpl

import models.template.templateModel as tm
import models.setting.settingModel as sm


@route("/admin/templates/(.*)")
class adminInfoTemplates(baseHTMLObject):
    __name__ = "admin templates"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        tmplid = self.env["members"][0]
        view = adminInfoTemplatesTmpl(searchList=[self.tmplSearchList])

        template = tm.formatTmpl(tm.templateORM.getByID(tmplid))
        view.scripts = ["handlebars_1.0.min",
                "adminModal.flagr",
                "sidebarTabs.flagr",
                "editForm.flagr",
                "adminInfoTemplates.flagr"]

        try:
            currentTypes = sm.getSetting("templates", "types")
        except:
            currentTypes = {"Set template types in settings"}

        view.templateTypes = currentTypes

        view.tmpl = template

        return view
