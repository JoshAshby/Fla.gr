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


@route("/admin/requests/(.*)/delete")
class adminDelRequests(baseHTMLObject):
    __name__ = "admin requests"
    __level__ = 50
    __login__ = True
    def POST(self):
        reqid = self.env["members"][0]

        req = rm.requestsORM.load(db.couchServer, reqid)
        db.couchServer.delete(req)

        self.head = ("303 SEE OTHER", [("location", "/admin/requests")])
        self.session.pushAlert("You deleted the request for `%s`!"%req.email, ":(", "warning")

