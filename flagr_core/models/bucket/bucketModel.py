#!/usr/bin/env python
"""
fla.gr bucket model

Basically what we have is a key value store in redis
of all the session ID's (store and retrieved via the cookie
from Seshat)

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import models.user.userModel as userModel
import models.baseModel as bum
import config.dbBase as db
import utils.dbUtils as dbu


class bucketPail(object):
    def __init__(self):
        self._buckets = []
        buckets = [ key.split(":value")[0] for key in db.redisBucketServer.keys("bucket:*:value") ]

        for bucket in buckets:
            redisBucket = bum.redisObject(bucket)
            if "users" in redisBucket:
                userList = []
                for user in redisBucket.users:
                    userList.append(userModel.getByID(user))
                redisBucket._userObjects = userList
            self._buckets.append(redisBucket)

    @staticmethod
    def toggle(bucketID):
        current = dbu.toBoolean(db.redisBucketServer.get("bucket:%s:value"%bucketID))
        return db.redisBucketServer.set("bucket:%s:value"%bucketID, not current)

    def __iter__(self):
        for bucket in self._buckets:
            yield bucket


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
