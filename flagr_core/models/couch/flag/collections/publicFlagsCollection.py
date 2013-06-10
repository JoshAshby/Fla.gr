#!/usr/bin/env python
"""
Collection specifically for dealing with a specific users private flags

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import models.redis.baseRedisModel as brm
import models.couch.baseCouchCollection as bcc
import models.couch.flag.flagModel as fm
import models.couch.user.userModel as um
import models.couch.flag.collections.userPublicFlagsCollection as pubfc
import config.config as c


class publicFlagsCollection(bcc.baseCouchCollection):
    """
    Attempts to provide a collection for `Documents` providing
    a way to customize the creation of each object, and a way to sort
    the objects by various fields. Inheriting classes should only need
    to override `preInitAppend` and `postInitAppend` currently.
    """
    def __init__(self, couch=c.database.couchServer):
        """
        Initializes the object, getting the list of ID's which will result in
        the collection being built when `fetch()` is called.

        :param model: A model which inherits from both `couchdb.Document`
            and `baseCouchModel`
        :param couch: The couchdb instance which this collection should use
        """
        self._collection = []
        self.couch = couch
        self.model = fm.flagORM
        self.pail = []
        self.update()

    def update(self):
        """
        Updates the internal list of objects, stored in a couch list, deleting
        keys that no longer exist, and adding new keys that are not currently
        part of the collection.
        """
        userIDs = bcc.baseCouchCollection(um.userORM)
        for user in userIDs:
            userPail = pubfc.userPublicFlagsCollection(user)
            self.pail.extend(userPail.pail)

        print self.pail
