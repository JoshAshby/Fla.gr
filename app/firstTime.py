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
import models.couch.user.userModel as um
import gators.firstTimeGator as gator

import models.redis.baseRedisModel as brm
import models.redis.bucket.bucketModel as bm

config = gator.config()

def setup():
    print "Setting up fla.gr from config/initial.json..."
    #initialSetup()
    bucketSetup()
    print "Done"

def initialSetup():
    print "Setting up inital users"
    for user in config.initial.users:
        if um.userORM.find(user["username"]):
            print "\tSkipping user %s" % user["username"]
        else:
            newUser = um.userORM(user["username"], user["password"])
            print "\tAdding new user `%s`"%user["username"]
            print "\t\tpassword `%s`"%user["password"]
            if user.has_key("level"):
                print "\t\tlevel `%d`"%user["level"]
                newUser.level = user["level"]
            else:
                print "\t\tlevel `100` - god"
                newUser.level = 100
            newUser.save()


def bucketSetup():
    print "Now setting up buckets..."
    buckets = config.buckets
    for bucket in buckets:
        print "Adding Bucket:"
        print "\t"  + bucket
        print "\t" + str(buckets[bucket])
        newBucket = brm.redisObject("bucket:" + bucket)

        newBucket["name"] = buckets[bucket]["name"]
        newBucket["value"] = buckets[bucket]["value"]
        newBucket["description"] = buckets[bucket]["description"]

        if buckets[bucket].has_key("users"):
            newBucket["users"] = buckets[bucket]["users"]

    pail = bm.bucketPail("bucket:*:value")
    pail.update()


if __name__ == "__main__":
    setup()
