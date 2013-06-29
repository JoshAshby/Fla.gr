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
from seshat.baseHTMLObject import baseHTMLObject

import models.redis.bucket.bucketModel as bm
import json


@autoRoute()
@admin(100)
class index(baseHTMLObject):
    _title = "dev buckets"
    _defaultTmpl = "flagpole/dev/buckets/buckets"
    def GET(self):
        """
        """
        page = self.request.getParam("p")

        self.view.scripts = ["jquery.json-2.4.min",
                "devBucketsButtons.flagr"]

        pail = bm.bucketPail("bucket:*:value")
        pail.paginate(page, 25)
        pail.fetch()
        pail.sortBy("id")

        self.view.data = {"buckets": pail}

        return self.view

    def POST(self):
        self.head = ("200 OK", [("Content-Type", "application/json")])
        bucket = json.loads(self.env["members"]["json"])

        reply = bm.bucketPail.toggle(bucket["bucket"])

        return json.dumps({"status": reply, "bucket": bucket["bucket"]})
