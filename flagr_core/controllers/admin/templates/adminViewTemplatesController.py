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

from views.admin.templates.adminViewTemplatesTmpl import adminViewTemplatesTmpl

import config.dbBase as db
import models.template.templateModel as tm


@route("/admin/templates")
class adminViewTemplates(baseHTMLObject):
    __name__ = "admin templates"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        view = adminViewTemplatesTmpl(searchList=[self.tmplSearchList])

        templates = tm.formatTmpls(list(tm.templateORM.view(db.couchServer, 'typeViews/template')))
        view.scripts = ["handlebars_1.0.min", "jquery.json-2.4.min", "adminViewTemplates"]

        view.templates = templates

        return view
