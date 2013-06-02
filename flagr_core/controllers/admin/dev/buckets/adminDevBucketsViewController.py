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
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.admin.dev.adminDevViewBucketsTmpl import adminDevViewBucketsTmpl

import models.bucket.bucketModel as bm
import json


@autoRoute()
class adminDevBucketsIndex(baseHTMLObject):
    _title = "dev buckets"
    __level__ = 100
    __login__ = True
    def GET(self):
        """
        """
        view = adminDevViewBucketsTmpl(searchList=[self.tmplSearchList])

        view.scripts = ["jquery.json-2.4.min",
                "devBucketsButtons.flagr"]
        pail = bm.bucketPail()
        view.buckets = pail

        return view

    def POST(self):
        self.head = ("200 OK", [("Content-Type", "application/json")])
        bucket = json.loads(self.env["members"]["json"])

        reply = bm.bucketPail.toggle(bucket["bucket"])

        return json.dumps({"status": reply})
