#!/usr/bin/env python
"""
fla.gr main startup and controller app.

**THIS FILE GETS RAN**


http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import sys
import os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
import gators.updateGator as ug

import models.redis.baseRedisModel as brm
import models.redis.bucket.bucketModel as bm
update = ug.config()

def addBuckets():
    buckets = update.buckets
    for bucket in buckets:
        print "Adding Bucket:"
        print "    "  + bucket
        print "    " + str(buckets[bucket])
        newBucket = brm.redisObject("bucket:" + bucket)

        newBucket["name"] = buckets[bucket]["name"]
        newBucket["value"] = buckets[bucket]["value"]
        newBucket["description"] = buckets[bucket]["description"]

        if buckets[bucket].has_key("users"):
            newBucket["users"] = buckets[bucket]["users"]

    pail = bm.bucketPail("bucket:*:value")
    pail.update()

def setup():
    addBuckets()

if __name__ == "__main__":
    setup()
