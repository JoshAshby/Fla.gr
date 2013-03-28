#!/usr/bin/env python
"""
fla.gr controller to control which template is used for the invite emails
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import models.setting.settingModel as sm


@route("/admin/requests/settings")
class adminRequestsSettings(baseHTMLObject):
    __name__ = "admin requests"
    __level__ = 50
    __login__ = True
    def POST(self):
        """
        """
        if self.env["cfg"].enableRequests:
            tmplid = self.env["members"]["tmplid"] if self.env["members"].has_key("tmplid") else ""
            if tmplid:
                sm.setSetting("enableRequests", "tmplid", tmplid)
                self.session.pushAlert("We've updated the template you're wanting to use to send invites out...", "Got that done...", "success")

            self.head = ("303 SEE OTHER", [("Location", "/admin/requests")])
