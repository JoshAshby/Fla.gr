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
from seshat.baseObject import JSONObject

import models.redis.bucket.bucketModel as bm


@autoRoute()
@admin(100)
class toggle(JSONObject):
    def POST(self):
        bucket = self.request.id

        reply = bm.bucketPail.toggle(bucket)

        return {"status": reply, "bucket": bucket, "success": True}
