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
import models.request.requestSettingModel as rsm
import utils.emailUtils as eu


@route("/admin/requests/(.*)/edit")
class adminEditRequests(baseHTMLObject):
    __name__ = "admin requests"
    __level__ = 50
    __login__ = True
    def POST(self):
        reqid = self.env["members"][0]
        grant = True if (self.env["members"].has_key("grant") and self.env["members"]["grant"] == "grant") else False

        if grant:
            req = rm.requestORM.load(db.couchServer, reqid)
            tmplid = rsm.tmplid()

            try:
                eu.sendMessage(tmplid, {"email": req.email}, req.email, "fla.gr Invite")
                self.session.pushAlert("You grants the request for `%s`! A special email is on the way to them, as a result of your kind actions"%req.email, ":)", "success")
            except Exception as exc:
                self.session.pushAlert("OH NO! The grant message didn't send. Heres the error: %s"%exc, "FAILURE!" "error")

        self.head = ("303 SEE OTHER", [("location", "/admin/requests")])
