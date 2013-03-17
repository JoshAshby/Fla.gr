#!/usr/bin/env python
"""
fla.gr model to help with settings for requests.

This should become a full on settings model, or maybe it can be tied in with buckets...

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""

import config.dbBase as db

def tmplid():
    id = db.redisBucketServer.get("bucket:enableRequests:settings:tmpl")
    return id
