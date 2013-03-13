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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.dev.adminDevViewBucketsTmpl import adminDevViewBucketsTmpl

import models.bucket.bucketModel as bm
import json


@route("/admin/dev/buckets")
class adminDevViewBuckets(baseHTMLObject):
    __name__ = "dev buckets"
    __level__ = 100
    __login__ = True
    def GET(self):
        """
        """
        view = adminDevViewBucketsTmpl(searchList=[self.tmplSearchList])

        view.scripts = ["jquery.json-2.4.min", "devBucketsButtons"]
        view.buckets = bm.adminBucketDict()

        return view

    def POST(self):
        self.head = ("200 OK", [("Content-Type", "application/json")])
        bucket = json.loads(self.env["members"]["json"])

        reply = bm.adminBucketToggle(bucket["bucket"])

        return json.dumps({"status": reply})
