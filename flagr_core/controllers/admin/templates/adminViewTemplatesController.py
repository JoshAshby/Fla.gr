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

from views.admin.templates.adminViewTemplatesTmpl import adminViewTemplatesTmpl

import models.couch.template.templateModel as tm
import models.redis.setting.settingModel as sm
import models.couch.baseCouchCollection as bcc
import json


@autoRoute()
class adminTemplatesIndex(baseHTMLObject):
    _title = "admin templates"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        page = self.env["members"]["p"] \
                if self.env["members"].has_key("p") else 1
        view = adminViewTemplatesTmpl(searchList=[self.tmplSearchList])

        view.scripts = ["handlebars_1.0.min",
                "jquery.json-2.4.min",
                "sidebarTabs.flagr",
                "bulkCheck.flagr",
                "adminModal.flagr",
                "editForm.flagr",
                "adminViewTemplates.flagr",
                "dynamicInput.flagr"]

        templates = bcc.baseCouchCollection(tm.templateORM)
        templates.paginate(page, 25)
        templates.fetch()
        templates.format()

        view.templates = templates

        try:
            view.templateTypes = json.dumps(list(sm.getSetting("templates", "types")))
        except:
            view.templateTypes = json.dumps([])

        return view
