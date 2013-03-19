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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.templates.adminInfoTemplatesTmpl import adminInfoTemplatesTmpl

import config.dbBase as db
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

        template = tm.formatTmpl(tm.templateORM.load(db.couchServer,tmplid))
        view.scripts = ["handlebars_1.0.min", "adminInfoTemplates"]

        try:
            currentTypes = sm.getSetting("templates", "types")
        except:
            currentTypes = {"Set template types in settings"}

        view.templateTypes = currentTypes

        view.tmpl = template

        return view
