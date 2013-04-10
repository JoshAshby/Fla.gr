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
import config.config as c
import os
import json
import string
import random

import config.dbBase as db
import models.user.userModel as um
import models.setting.settingModel as sm


if os.path.exists(c.baseFolder+'/siteConfig.json'):
    siteConfigFile = open(c.baseFolder+"/siteConfig.json")
    siteConfig = json.loads(siteConfigFile.read())

    buckets = siteConfig["buckets"]
    settings = siteConfig["settings"]
    initial = siteConfig["initial"]
else:
    raise Exception("No siteConfig.json found, stopping first time process...")

def setup():
    """
    Wrapper function for calling the needed setup tasks.
    """
    print "Setting up fla.gr from siteConfig.json..."
    initialSetup()
    bucketSetup()
    settingSetup()
    print "Done"

def initialSetup():
    """
    Sets up the initial user and flags in the system, as defined by the
    users and flags keys in the siteConfig.json
    """
    print "Setting up inital user and flags..."
    if initial.has_key("users"):
        for user in initial["users"]:
            if not um.userORM.find(user["username"]):
                newUser = um.userORM(user["username"], user["password"])
                print "\tAdding new user `%s`"%user["username"]
                print "\t\tpassword `%s`"%user["password"]
                if user.has_key("level"):
                    print "\t\tlevel `%d`"%user["level"]
                    newUser.level = user["level"]
                else:
                    print "\t\tlevel `100`"
                    newUser.level = 100
                newUser.save()
            else:
                print "\tUser `%s` already in system, skipping..."%user["username"]

    if initial.has_key("flags"):
        pass

def settingSetup():
    """
    Handles setting up the system settings from the siteConfig.json
    """
    print "Setting up settings..."
    for key in settings:
        settingsBits = settings[key]
        for bit in settingsBits:
            setting = settingsBits[bit]
            try:
                sm.getSetting(key, bit)
                print "\tKey `%s:%s` exists, skipping..."%(key, bit)
            except:
                if type(setting) == str and \
                        setting == "generateRandom":
                    print "\tGenerating random string for key: `%s:%s`"%(key, bit)
                    setting = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(25))
                if type(setting) == list:
                    setting = set(setting)

                sm.setSetting(key, bit, setting)
                print "\tSet key `%s:%s` to `%s`"%(key, bit, setting)

def bucketSetup():
    """
    Sets up the buckets in redis with the name, description, and initial value.
    """
    print "Now setting up redis buckets..."

    keys = db.redisBucketServer.keys("bucket:*")
    currentBucketKeys = []
    for key in keys:
        key = key.split(":")[1]
        currentBucketKeys.append(key)

    currentBucketKeys = list(set(currentBucketKeys))

    if currentBucketKeys:
        print "\tCurrent buckets in the database:"
        for key in currentBucketKeys:
            print "\t\t%s"%key
    else:
        print "\tNo buckets found in the database, adding buckets..."

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
        print "\tNo new buckets to add, skipping step..."


if __name__ == "__main__":
    setup()
