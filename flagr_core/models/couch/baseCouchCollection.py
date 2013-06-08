#!/usr/bin/env python
"""
base collection classes for building collections of model objects

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import models.redis.baseRedisModel as brm
import models.baseCollection as bc
import config.config as c


class baseCouchCollection(bc.baseCollection):
    """
    Attempts to provide a collection for `Documents` providing
    a way to customize the creation of each object, and a way to sort
    the objects by various fields. Inheriting classes should only need
    to override `preInitAppend` and `postInitAppend` currently.
    """
    def __init__(self, model, couch=c.database.couchServer):
        """
        Initializes the object, getting the list of ID's which will result in
        the collection being built when `fetch()` is called.

        :param model: A model which inherits from both `couchdb.Document`
            and `baseCouchModel`
        :param couch: The couchdb instance which this collection should use
        """
        self._collection = []
        self.couch = couch
        self.model = model
        self.pattern = "couch:" + self.model._name
        self.pail = brm.redisList(self.pattern)
        if not self.pail:
            self.update()

    def fetch(self):
        """
        Fetches the documents
        """
        pail = self.pagination if hasattr(self, "pagination") else self.pail
        for drop in pail:
            drip = self.model.getByID(drop)

            drip = self.preInitAppend(drip)
            self._collection.append(drip)
            self.postInitAppend()

    def addObject(self, key):
        """
        Adds an object to the internal list object, stored in a couch list

        :param key: The key of the object, in the form of `id` as `what:` is
            supplied by the collection
        :type key: Str
        """
        self.pail.append(key)

    def delObject(self, key):
        """
        Removes an object to the internal list of objects, stored in a couch list

        :param key: The key of the object, in the form of `id` as `what:` is
            supplied by the collection
        :type key: Str
        """
        self.pail.remove()

    def update(self):
        """
        Updates the internal list of objects, stored in a couch list, deleting
        keys that no longer exist, and adding new keys that are not currently
        part of the collection.
        """
        pail = [ item.id for item in self.model.all() ]

        delete = (self.pail == [])

        for drop in pail:
            if drop not in self.pail:
                self.pail.append(drop)

        if delete:
            for drop in self.pail:
                if drop not in pail:
                    self.pail.remove(drop)
