#!/usr/bin/env python
"""
fla.gr controller for view a list of current invite requests
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.requests.adminViewRequestsTmpl import adminViewRequestsTmpl

import config.dbBase as db
import models.request.requestModel as rm
import models.template.templateModel as tm
import models.setting.settingModel as sm


@route("/admin/requests")
class adminViewRequests(baseHTMLObject):
    __name__ = "admin requests"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            view = adminViewRequestsTmpl(searchList=[self.tmplSearchList])

            requests = rm.formatRequests(rm.requestORM.all())

            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "sidebarTabs.flagr",
                    "adminModal.flagr",
                    "bulkCheck.flagr",
                    "editForm.flagr",
                    "adminViewRequests.flagr"]

            view.requests = requests

            try:
                currentTmpl = sm.getSetting("enableRequests", "tmplid")
            except:
                currentTmpl = ""

            tmpls = list(tm.templateORM.view(db.couchServer, 'typeViews/template'))
            for tmpl in tmpls:
                if tmpl.type != "email":
                    tmpls.pop(tmpls.index(tmpl))
                else:
                    tmpl.current = False
                    if tmpl.id == currentTmpl:
                        tmpl.current = True

            view.tmpls = tmpls

            return view
        else:
            self.head = ("404 NOT FOUND", [])
