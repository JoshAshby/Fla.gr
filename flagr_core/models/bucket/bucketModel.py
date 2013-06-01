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
        for additional in ["users", "requires", "disables"]:
            if db.redisBucketServer.exists("%s:%s"%(bucket, additional)):
                if db.reditBucketServer.type("%s:%s"(bucket, additional)) == "set":
                    bits = db.redisBucketServer.smembers("%s:%s"(bucket, additional))
                    bitList = []
                    for bit in bits:
                        if additional == "users":
                            bitList.append(userModel.getByID(bit))
                        else:
                            bitList.append(bit)
                    returnBuckets[bucket.strip("bucket").strip(":")][additional] = bitList

    return returnBuckets



def adminBucketToggle(bucketID):
    current = dbu.toBoolean(db.redisBucketServer.get("bucket:%s:value"%bucketID))
    return db.redisBucketServer.set("bucket:%s:value"%bucketID, not current)


class redisObject(object):
    """
    I said I never would, but this is another attempt at making
    an ORM for redis...
    It's probably not going to work, but heres hopping.
    """
    def __init__(self, what, itemID=None):
        self._keys = {}
        if id:
            self._id = itemID
            bits = db.redisBucketServer.keys("%s:%s:*"%(what, itemID))
            for bit in bits:
                objectPart = bit.strip("%s:%s:"%(what, itemID))
                objectType = db.redisBucketServer.type(bit)

                if objectType == "string":
                    objectValue = db.redisServer.get(bit)
                    try:
                        objectValue = dbu.toBoolean(objectValue)
                    except:
                        pass
                    self._keys[objectPart] = objectValue
                elif objectType == "set":
                    self._keys[objectPart] = redisSet(bit)
                elif objectType == "list":
                    self._keys[objectPart] = redisList(bit)

    @classmethod
    def new(cls, what, itemID, **kwargs):
        newObject = cls(what, itemID)
        for kwarg in kwargs:
            newObject._keys[kwarg] = kwargs[kwarg]
        return newObject

    @classmethod
    def getById(cls, what, itemID):
        return cls(itemID)

    def __getattr__(self, item):
        if item in self._keys:
            return self._keys[item]
        return object.__getattribute__(self, item)

    def __getitem__(self, item):
        if item in self._keys:
            return self._keys[item]
        return object.__getattribute__(self, item)

    def __setattr__(self, item, value):
        if item in self._keys and not hasattr(value, '__call__'):
            self._keys[item] = value
            return self._keys[item]
        return object.__setattr__(self, item, value)

    def __setitem__(self, item, value):
        if item in self._keys and not hasattr(value, '__call__'):
            self._keys[item] = value
            return self._keys[item]
        return object.__setattr__(self, item, value)


class redisList(object):
    def __init__(self):
        self._list = []


class redisSet(object):
    def __init__(self):
        self._set = set()


class redisSortedSet(object):
    def __init__(self):
        """
        We store the sorted list as a dictonary in python,
        where the key is the rank, and the value is the list item
        """
        self._list = {}


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
