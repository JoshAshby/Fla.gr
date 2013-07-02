#!/usr/bin/env python
"""
fla.gr controller for view a list of current invite requests

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseHTMLObject import HTMLObject
from seshat.objectMods import *

import models.couch.request.requestModel as rm
import models.couch.baseCouchCollection as bcc

from views.template import listView, paginateView


@autoRoute()
@admin()
class index(HTMLObject):
    _title = "admin requests"
    _defaultTmpl = "flagpole/requests/requests"
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            page = self.request.getParam("page", 1)
            perpage = self.request.getParam("perpage", 25)
            sort = self.request.getParam("sort", "title")

            self.view.scripts = ["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "modal.flagr",
                    "flagpole/requests.flagr"]

            requests = bcc.baseCouchCollection(rm.requestORM)
            requests.paginate(page, perpage)
            requests.fetch()
            requests.format()
            requests.sortBy(sort)

            requestsList = listView("flagpole/partials/rows/flag", requests)
            pagination = paginateView(requests)

            self.view.data = {"requests": requestsList,
                "pagination": pagination}

            return self.view
        else:
            self._404()
