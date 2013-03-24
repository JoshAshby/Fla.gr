#!/usr/bin/env python
"""
fla.gr base model with a few classmethods and such to help
    keep a general interface across all models


http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.dbBase as db


class baseCouchModel(object):
    def __init__(self, **kwargs):
        pass

    def save(self):
        """
        Simply a shortcut for saving the document to couch
        """
        self.store(db.couchServer)

    @classmethod
    def getByID(cls, ID):
        """
        If you already know the id of the document you want, then just call
        this and it'll return that document

        :param ID: The document id of the document you want to retrieve
        :return: An instance of `cls` which has the matching document id
        """
        return cls.load(db.couchServer, ID)

    @classmethod
    def findWithView(cls, view, value):
        """
        Searches couchdb for documents that have the requested username

        :param value: The value to search for in the ORM
        :return: Either a `cls` instance or a list of `cls` instances
            if a result or multiple have been found.
            `None` if no user is found
        """
        items = cls.getAll(view, key=value)
        if items:
            if len(items.rows) == 1:
                return items.rows[0]
            else:
                return items.rows
        else:
            items = cls.getAll(view)
            if not items:
                return None
            return cls._search(items, value)

    @classmethod
    def getAll(cls, view, key=None):
        """
        Returns either all of the documents under view, or all of the documents
        which match the key
        :param view: The name of the view to use, currently this is the name of the
            couchdb view, however it can be extended into other areas later on if I
            ever change the underlying database.
        :param key: Optional view key to use
        :return: A list of ORM instances which fall within the given `view`
        """
        if key:
            return cls.view(db.couchServer, view, key=key)
        return cls.view(db.couchServer, view)
