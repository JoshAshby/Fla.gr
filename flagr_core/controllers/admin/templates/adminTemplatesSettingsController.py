#!/usr/bin/env python
"""
fla.gr controller for editing template settings
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

import models.setting.settingModel as sm
import json


@route("/admin/templates/settings")
class adminTemplatesSettings(baseHTMLObject):
    __name__ = "admin templates"
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
