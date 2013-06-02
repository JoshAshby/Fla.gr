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
import models.baseModel as bum
import config.dbBase as db


class baseRedisCollection(object):
    def __init__(self, pattern, redis=db.redisBucketServer):
        """
        Assumes the redis objects are stored in a pattern of `what:id:parts``
        Where `what` is like a class, where all keys in `what` are of the same
        object type in the system.

        :param pattern: The pattern which to find all the keys in this collection
            For example, `bucket:*:value` is a general pattern to find all the ids
            in the category of `bucket`
        """
        self._collection = []
        self.redis = redis
        self.pattern = pattern
        key = pattern.split(":")[0] + ":"
        pail = list(set([ key+item.split(":")[1] for item in self.redis.keys(self.pattern) ]))

        for drop in pail:
            drip = bum.redisObject(drop)
            drip = self.preInitAppend(drip)
            self._collection.append(drip)
            self.postInitAppend()

    def preInitAppend(self, drip):
        return drip

    def postInitAppend(self):
        pass

    def sortBy(self, by, order='DESC'):
        self._collection.sort(key=lambda x: x[by])
        if order is not 'DESC':
            self._collection.reverse()
        return self._collection

    def __iter__(self):
        for drip in self._collection:
            yield drip

