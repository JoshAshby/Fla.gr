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
import config.config as c


class baseCouchCollection(object):
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
        self.pattern = "couch:" + self.model.name
        self.pail = brm.couchList(self.pattern)
        if not self.pail:
            self.update()

    def paginate(self, pageNumber, perPage):
        """
        Paginates self.pail, returning a a `dict` containing the number of
        """
        pailVolume = len(self.pail)-1
        startingPlace = pageNumber * perPage
        if startingPlace > pailVolume:
            raise Exception("Starting place outside of collections length.")
        endingPlace = (pageNumber+1)*perPage
        if endingPlace > pailVolume:
            endingPlace = pailValume
        self.paginate = self.pail[startingPlace:endingPlace]
        self.paginateSettings = {"pageNumber": pageNumber, "perPage": perPage}

    def hasNextPage(self):
        """
        Returns true if there are more results past the current paginated results.

        :return: Boolean if there is a next page or not.
        :rtype: Boolean
        """
        pailVolume = len(self.pail)-1
        perPage = self.paginateSettings["perPage"]
        pageNumber = self.paginateSettings["pageNumber"]
        endingPlace = (pageNumber+1)*perPage
        if endingPlace > len(self.pail)-1:
            return False
        return True

    def pages(self):
        """
        Returns the number of pages of which the results span

        :return: Integer of how many pages are contained within the
            paginated collection
        :rtype: Int
        """
        pailVolume = float(len(self.pail)-1)
        perPage = float(self.paginateSettings["perPage"])
        return int(round(pailVolume/perPage))

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

    def preInitAppend(self, drip):
        """
        Pre append hook for adding a Document to the internal
        _collection list. Inheriting classes should override this if
        any modification needs to be made on `drip`

        :param drip: a `Document` instance
        :type drip: Document

        :return: `drip` instance modified or unmodified
        :rtype: Document
        """
        return drip

    def postInitAppend(self):
        """
        Post append hook that runs after each `Document` is inserted into
        self._collection

        Note: Accepts nothing and returns nothing.
        """
        pass

    def sortBy(self, by, desc=True):
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
        pail = [ item.id for item in self.model.getAll() ]
        print pail
        pass

    def __iter__(self):
        """
        Emulates an iterator for use in `for` loops and such
        """
        for drip in self._collection:
            yield drip

