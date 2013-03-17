#!/usr/bin/env python
"""
fla.gr controller to control which template is used for the invite emails

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.requests.adminRequestsSettingsTmpl import adminRequestsSettingsTmpl

import models.request.requestSettingModel as rsm


@route("/admin/requests/settings")
class adminRequestsSettings(baseHTMLObject):
    __name__ = "admin requests"
    __level__ = 50
    __login__ = True
    def GET(self):
        """
        """
        view = adminRequestsSettingsTmpl(searchList=[self.tmplSearchList])

        tmpl = rsm.tmpls()

        view.tmpl = tmpl

        return view
