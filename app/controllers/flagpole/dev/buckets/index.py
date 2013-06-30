#!/usr/bin/env python
"""
fla.gr controller for view a list of current cfg buckets

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.objectMods import *
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject

import models.redis.bucket.bucketModel as bm

from views.template import listView, paginateView

@autoRoute()
@admin(100)
class index(HTMLObject):
    _title = "dev buckets"
    _defaultTmpl = "flagpole/dev/buckets/buckets"
    def GET(self):
        """
        """
        page = self.request.getParam("page", 1)
        perpage = self.request.getParam("perpage", 25)
        sort = self.request.getParam("sort", "id")

        self.view.scripts = ["handlebars_1.0.min",
            "modal.flagr",
            "flagpole/buckets.flagr"]

        pail = bm.bucketPail("bucket:*:value")
        pail.paginate(page, perpage)
        pail.fetch()
        pail.sortBy(sort)

        buckets = listView("flagpole/partials/rows/bucket", pail)
        pagination = paginateView(pail)

        self.view.data = {"buckets": buckets,
            "pagination": pagination}

        return self.view
