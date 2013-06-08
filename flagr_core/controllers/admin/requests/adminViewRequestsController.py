#!/usr/bin/env python
"""
fla.gr controller for view a list of current invite requests

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.admin.requests.adminViewRequestsTmpl import adminViewRequestsTmpl

import models.couch.request.requestModel as rm
import models.couch.template.templateModel as tm
import models.redis.setting.settingModel as sm
import models.couch.baseCouchCollection as bcc


@autoRoute()
class adminRequestsIndex(baseHTMLObject):
    _title = "admin requests"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            view = adminViewRequestsTmpl(searchList=[self.tmplSearchList])

            view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "sidebarTabs.flagr",
                    "adminModal.flagr",
                    "bulkCheck.flagr",
                    "editForm.flagr",
                    "adminViewRequests.flagr"]

            requests = bcc.baseCouchCollection(rm.requestORM)
            requests.paginate(1, 25)
            requests.fetch()
            requests.format()

            view.requests = requests

            try:
                currentTmpl = sm.getSetting("enableRequests", "tmplid")
            except:
                currentTmpl = ""

            tmpl = bcc.baseCouchCollection(tm.templateORM)
            tmpl.fetch()
            tmpl.filterBy("type", "email")
            for tmp in tmpl:
                if tmp.id == currentTmpl:
                    tmp.current = True

            view.tmpls = tmpl

            return view
        else:
            self._404()
