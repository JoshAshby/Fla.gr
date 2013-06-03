#!/usr/bin/env python
"""
base collection classes for building collections of model objects

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import models.redis.baseRedisModel as bum
import config.config as c


class baseRedisCollection(object):
    """
    Attempts to provide a collection for `redisObjects` providing
    a way to customize the creation of each object, and a way to sort
    the objects by various fields. Inheriting classes should only need
    to override `preInitAppend` and `postInitAppend` currently.

    For an example see `bucketsPail` in `models.bucket.bucketModel`
    """
    def __init__(self, pattern, redis=c.database.redisBucketServer):
        """
        Assumes the Redis objects are stored in a pattern of `what:id:parts``
        Where `what` is like a class, where all keys in `what` are of the same
        object type in the system.

        :param pattern: The pattern which to find all the keys in this collection
            For example, `bucket:*:value` is a general pattern to find all the ids
            in the category of `bucket`

        :param redis: The Redis instance which this collection should use
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
        """
        Pre append hook for adding a redisObject to the internal
        _collection list. Inheriting classes should override this if
        any modification needs to be made on `drip`

        :param drip: a `redisObject` instance
        :type drip: redisObject

        :return: `drip` instance modified or unmodified
        :rtype: redisObject
        """
        return drip

    def postInitAppend(self):
        """
        Post append hook that runs after each `redisObject` is inserted into
        self._collection

        Note: Accepts nothing and returns nothing.
        """
        pass

    def sortBy(self, by, desc=False):
        """
        Sorts the collection by the field specified in `by`

        :param by: The name of the field by which the collection should be
            sorted by
        :type by: Str

        :param desc: If false then the collection is sorted then revered.
        :type desc: Boolean

        :return: The collection after sorting
        :rtype: List
        """
        self._collection.sort(key=lambda x: x[by])
        if not desc:
            self._collection.reverse()
        return self._collection

    def __iter__(self):
        """
        Emulates an iterator for use in `for` loops and such
        """
        for drip in self._collection:
            yield drip

