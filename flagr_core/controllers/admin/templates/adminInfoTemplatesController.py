#!/usr/bin/env python
"""
fla.gr controller for view a list of current templates

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.admin.templates.adminInfoTemplatesTmpl import adminInfoTemplatesTmpl

import models.couch.template.templateModel as tm
import models.redis.setting.settingModel as sm


@autoRoute()
class adminTemplatesView(baseHTMLObject):
    _title = "admin templates"
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
