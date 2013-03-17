#!/usr/bin/env python
"""
Aid to get flagr setup and running

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.dbBase as db
import models.user.userModel as um

import string
import random


buckets = {"enableDynamicLabels": {"value": True, "name": "New label input for flags", "description": "Enables a new, more interactive way to add and remove labels from a flag while editing, or making a new flag."},
        "enableRequests": {"value": False, "name": "Request and invite managment", "description": "Enables pages for requesting an invite while the site is in a closed beta or alpha, and adds an admin tab for managing the requests."},
        "enableModalFlagDeletes": {"value": True, "name": "Single page flag delete", "description": "Enabled a modal for the deleting process of a flag, instead of directing the user to another page."}}

def setup():
    if not um.findUserByUsername("Admin") and not um.findUserByUsername("Josh"):
        print "Now making a new admin user..."
        print "\tusername: `Admin`"
        print "\tpassword: `admin`"
        newUser = um.userORM.new(username="Admin", password="admin")
        newUser.level = 100
        newUser.save()

    print "Now setting up redis buckets..."

    keys = db.redisBucketServer.keys("bucket:*")
    currentBucketKeys = []
    for key in keys:
        key = key.split(":")[1]
        currentBucketKeys.append(key)

    currentBucketKeys = list(set(currentBucketKeys))

    if currentBucketKeys:
        print "Current buckets in the database:"
        for key in currentBucketKeys:
            print "\t%s"%key
    else:
        print "No buckets found in the database, adding buckets..."

    bucketKeys = []
    for bucket in buckets:
        bucketKeys.append(bucket)

    if currentBucketKeys != bucketKeys:
        for key in bucketKeys:
            if key not in currentBucketKeys:
                print "\tAdding bucket `%s` to buckets..."%key
                db.redisBucketServer.set("bucket:%s:value"%key, buckets[key]["value"])
                db.redisBucketServer.set("bucket:%s:name"%key, buckets[key]["name"])
                db.redisBucketServer.set("bucket:%s:description"%key, buckets[key]["description"])
    else:
        print "No new buckets to add, skipping step..."

    if buckets["enableRequests"]["value"]:
        print "Now generating request secret key..."

        secret = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(25))
        db.redisBucketServer.set("requestSecret", secret)

    print "All done!"


if __name__ == "__main__":
    setup()
