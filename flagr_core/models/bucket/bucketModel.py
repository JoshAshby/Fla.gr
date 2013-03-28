#!/usr/bin/env python
"""
fla.gr bucket model

Basically what we have is a key value store in redis
of all the buckets, and we just pull in all that info as
a dict in python, for processing.
"""
import models.user.userModel as userModel
import config.dbBase as db
import utils.dbUtils as dbu


def adminBucketDict():
    """
    Attempts to make a single dict which holds the description and
    value for each bucket as the value, and the id of the bucket as the key.
    eg:
        {"id0": {"value": True, "description":"description goes here", "name": "enable id0"}}

    :return: A dict of ids and another dict. Each value is a smaller dict of the key value,
        name and description
    """
    returnBuckets = dict()

    buckets = [ key.strip(":value") for key in db.redisBucketServer.keys("bucket:*:value") ]

    for bucket in buckets:
        returnBuckets[bucket.strip("bucket").strip(":")] = {"value": dbu.toBoolean(db.redisBucketServer.get(bucket+":value")),
                "name": db.redisBucketServer.get(bucket+":name"),
                "description": db.redisBucketServer.get(bucket+":description")}
        #Finally attach a list of userORM objects for the users who have access to this bucket
        if db.redisBucketServer.exists("%s:users"%bucket):
            users = db.redisBucketServer.smembers("%s:users")
            userList = []
            for user in users:
                userList.append(userModel.getByID(user))
            returnBuckets[bucket.strip("bucket").strip(":")]["users"] = userList

    return returnBuckets



def adminBucketToggle(bucketID):
    current = dbu.toBoolean(db.redisBucketServer.get("bucket:%s:value"%bucketID))
    return db.redisBucketServer.set("bucket:%s:value"%bucketID, not current)


class cfgBuckets(object):
    def __init__(self):
        keys = { key.split(":")[1]:dbu.toBoolean(db.redisBucketServer.get(key)) for key in db.redisBucketServer.keys("bucket:*:value") }
        for key in keys:
            setattr(self, key, keys[key])

    def __getattr__(self, item):
        return object.__getattribute__(self, item)

    def __getitem__(self, item):
        return object.__getattribute__(self, item)

    def __setattr__(self, item, value):
        return object.__setattr__(self, item, value)

    def __setitem__(self, item, value):
        return object.__setattr__(self, item, value)
