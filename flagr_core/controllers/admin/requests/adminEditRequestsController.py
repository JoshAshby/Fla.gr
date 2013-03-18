#!/usr/bin/env python
"""
fla.gr controller for editing a request
Currently this only will grant a request

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import models.request.requestModel as rm
import models.request.requestSettingModel as rsm
import utils.email.emailUtils as eu
import json


@route("/admin/requests/grant")
class adminEditRequests(baseHTMLObject):
    __name__ = "admin requests"
    __level__ = 50
    __login__ = True
    def POST(self):
        ids = json.loads(self.env["members"]["array"]) if self.env["members"].has_key("array") else []

        tmplID = rsm.tmplid()

        tmplData = {}
        emails = []

        for ID in ids:
            req = rm.requestORM.findByID(ID)
            #generate register key here...
            tmplData[req.email] = {"email": req.email, "registerID": ""}
            emails.append(req.email)

        try:
            eu.sendMessage(tmplID, tmplData, emails, "fla.gr Invite")
            self.session.pushAlert("You granted the requests! A special email is on the way to them, as a result of your kind actions", ":)", "success")
        except Exception as exc:
            self.session.pushAlert("OH NO! One or all of the grant messages didn't send. Heres the error: %s"%exc, "FAILURE!" "error")

        self.head = ("303 SEE OTHER", [("location", "/admin/requests")])
