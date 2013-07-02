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
from seshat.baseObject import HTMLObject
from seshat.objectMods import *

import models.couch.request.requestModel as rm

import json


@autoRoute()
@admin()
class delete(HTMLObject):
    _title = "admin requests"
    def POST(self):
        if self.request.cfg.enableRequests:
            ID = self.request.id

            req = rm.requestORM.find(ID)
            req.delete()

            self.head = ("303 SEE OTHER", [("location", "/flagpole/requests")])
            self.request.session.pushAlert("You deleted those requests...", ":(", "warning")
        else:
            self._404()
