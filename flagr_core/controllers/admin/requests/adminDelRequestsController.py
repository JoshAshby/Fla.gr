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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import config.dbBase as db
import models.request.requestModel as rm
import json


@route("/admin/requests/delete")
class adminDelRequests(baseHTMLObject):
    __name__ = "admin requests"
    __level__ = 50
    __login__ = True
    def POST(self):
        if self.env["cfg"].enableRequests:
            ids = json.loads(self.env["members"]["array"]) if self.env["members"].has_key("array") else []

            for ID in ids:
                req = rm.requestORM.findByID(ID)
                db.couchServer.delete(req)

            self.head = ("303 SEE OTHER", [("location", "/admin/requests")])
            self.session.pushAlert("You deleted those requests...", ":(", "warning")
        else:
            self.head = ("404 NOT FOUND", [])
