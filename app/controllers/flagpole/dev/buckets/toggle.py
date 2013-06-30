#!/usr/bin/env python
"""
fla.gr controller for toggling said buckets

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
class toggle(baseHTMLObject):
    _title = "dev buckets"
    def POST(self):
        self.head = ("200 OK", [("Content-Type", "application/json")])
        bucket = self.request.id

        reply = bm.bucketPail.toggle(bucket)

        return json.dumps({"status": reply, "bucket": bucket, "success": True})
