#!/usr/bin/env python
"""
fla.gr base model with a few classmethods and such to help
    keep a general interface across all models
"""
import config.dbBase as db


class baseCouchModel(object):
    """
    Extension of the couchdb-python Document class to provide a
    bit more of an object interface with the documents, since some
    things such as saving and deleteing the documents doesn't feel
    very object based to me.
    """
    def __init__(self, **kwargs):
        pass

    @classmethod
    def new(cls, **kwargs):
        """
        
        """
        return cls(**kwargs)

    def save(self):
        """
        Simply a shortcut for saving the document to couch
        """
        self.store(db.couchServer)

    def delete(self):
        """
        Deletes the current instance
        """
        db.couchServer.delete(self)

    @classmethod
    def getByID(cls, ID):
        """
        If you already know the id of the document you want, then just call
        this and it'll return that document

        :param ID: The document id of the document you want to retrieve
        :type ID: Str
        :return: An instance of `cls` which has the matching document id
        :rtype: cls instance
        """
        return cls.load(db.couchServer, ID)

    @classmethod
    def findWithView(cls, view, value):
        """
        Searches couchdb for documents that have the requested username

        :param value: The value to search for in the ORM
        :type value: Str
        :return: Either a `cls` instance or a list of `cls` instances
            if a result or multiple have been found.
            `None` if no user is found
        :rtype: cls instance
        """
        items = cls.getAll(view, key=value)
        if items:
            if len(items) == 1:
                return items[0]
            else:
                return items
        else:
            items = cls.getAll(view)
            if not items:
                return None
            return cls._search(items, value)

    @classmethod
    def find(cls, value):
        """
        Searches couchdb for documents that have the requested username

        :param value: The value to search for in the ORM
        :type value: Str
        :return: Either a `cls` instance or a list of `cls` instances
            if a result or multiple have been found.
            `None` if no user is found
        :rtype: cls instance
        """
        return cls.findWithView(cls._view, value)

    @classmethod
    def getAll(cls, view, key=None):
        """
        Returns either all of the documents under view, or all of the documents
        which match the key

        :param view: The name of the view to use, currently this is the name of the
            couchdb view, however it can be extended into other areas later on if I
            ever change the underlying database.
        :type view: Str
        :param key: Optional view key to use
        :type key: Str
        :return: A list of ORM instances which fall within the given `view`
        :rtype: List 
        """
        if key:
            return list(cls.view(db.couchServer, view, key=key))
        return list(cls.view(db.couchServer, view))

    @classmethod
    def all(cls):
        """
        Returns a list of all the documents which are with in cls._view
        This is mainly a wrappper function, using the classes _view so you
        don't have to remember which view your working with.

        :return: List of all documents within cls._view
        :rtype: List
        """
        return cls.getAll(cls._view)
