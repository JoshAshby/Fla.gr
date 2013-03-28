#!/usr/bin/env python
"""
fla.gr controller for view a list of current cfg buckets
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.admin.dev.adminDevViewBucketsTmpl import adminDevViewBucketsTmpl

import models.bucket.bucketModel as bm
import json


@route("/admin/dev/buckets")
class adminDevViewBuckets(baseHTMLObject):
    """
    Handles the enabling and disabling of buckets for fla.gr

     * Must be logged in
     * Must be level 100 or more
    """
    __name__ = "dev buckets"
    __level__ = 100
    __login__ = True
    def GET(self):
        """
        Presents a page containing a list of buckets, and a button/modal system
        which allowes the user to toggle the functionality of the buckets within fla.gr
        """
        view = adminDevViewBucketsTmpl(searchList=[self.tmplSearchList])

        view.scripts = ["jquery.json-2.4.min",
                "devBucketsButtons.flagr"]
        view.buckets = bm.adminBucketDict()

        return view

    def POST(self):
        """
        Toggles the state of the bucket.

        :member json: A JSON object of the bucket name, description and ID
        """
        self.head = ("200 OK", [("Content-Type", "application/json")])
        bucket = json.loads(self.env["members"]["json"])

        reply = bm.adminBucketToggle(bucket["bucket"])

        return json.dumps({"status": reply})
