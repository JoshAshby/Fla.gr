#!/usr/bin/env python
"""
fla.gr controller for editing template settings

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

import models.redis.setting.settingModel as sm
import json


@autoRoute()
class adminTemplatesSettings(baseHTMLObject):
    _title = "admin templates"
    __level__ = 50
    __login__ = True
    def POST(self):
        labels = self.env["members"]["addInput"] or "[]"

        labels = set(json.loads(labels))

        try:
            sm.setSetting("templates", "types", labels)
            self.session.pushAlert("Template types updated", "Yay", "success")
        except Exception as exc:
            self.session.pushAlert("Couldn't set the template types... %s"%exc, "wha'oh", "error")

        self.head = ("303 SEE OTHER",
            [("location", "/admin/templates")])
