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
import models.setting.settingModel as sm

import string
import random


siteConfig = {}
if os.path.exists(baseFolder+'/siteConfig.json'):
    siteConfigFile = open(baseFolder+"/siteConfig.json")
    siteConfig = json.loads(siteConfigFile.read())

    buckets = siteConfig["buckets"]
else:
    raise Exception("No siteConfig.json found, stopping first time process...")

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

    try:
        sm.getSetting("enableRequests", "requestSecret")
        print "Secret for requests already made, skipping..."

    except:
        print "Now generating request secret key..."

        secret = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(25))
        sm.setSetting("enableRequests", "requestSecret", secret)

    print "All done!"


if __name__ == "__main__":
    setup()
