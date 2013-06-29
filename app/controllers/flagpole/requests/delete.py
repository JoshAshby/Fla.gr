#!/usr/bin/env python
"""
fla.gr controller for deleting a request

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

import models.couch.request.requestModel as rm

import json


@autoRoute()
class adminRequestsDelete(baseHTMLObject):
    _title = "admin requests"
    __level__ = 50
    __login__ = True
    def POST(self):
        if self.env["cfg"].enableRequests:
            ids = json.loads(self.env["members"]["array"]) if self.env["members"].has_key("array") else []

            for ID in ids:
                req = rm.requestORM.find(ID)
                req.delete()

            self.head = ("303 SEE OTHER", [("location", "/admin/requests")])
            self.session.pushAlert("You deleted those requests...", ":(", "warning")
        else:
            self._404()