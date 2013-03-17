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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.requests.adminViewRequestsTmpl import adminViewRequestsTmpl

import config.dbBase as db
import models.request.requestModel as rm


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

            requests = rm.formatRequests(list(rm.requestORM.view(db.couchServer, 'typeViews/request')))

            view.scripts = ["handlebars_1.0.min", "adminViewRequests"]

            view.requests = requests

            return view
        else:
            self.head = ("404 NOT FOUND", [])
