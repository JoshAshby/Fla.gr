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
import utils.dbUtils as dbu


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
        :return: Either a `cls` instance or a list of `cls` instances
            if a result or multiple have been found.
            `None` if no user is found
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
        :param key: Optional view key to use
        :return: A list of ORM instances which fall within the given `view`
        """
        if key:
            return list(cls.view(db.couchServer, view, key=key))
        return list(cls.view(db.couchServer, view))

    @classmethod
    def all(cls):
        return cls.getAll(cls._view)


class redisObject(object):
    """
    I said I never would, but this is another attempt at making
    an ORM for redis...
    It's probably not going to work, but heres hopping.
    """
    def __init__(self, what, itemID=None, redis=db.redisBucketServer):
        self._keys = {}
        self.redis = redis
        if id:
            self._id = itemID
            bits = self.redis.keys("%s:%s:*"%(what, itemID))
            for bit in bits:
                objectPart = bit.strip("%s:%s:"%(what, itemID))
                objectType = self.redis.type(bit)

                if objectType == "string":
                    objectValue = self.redis.get(bit)
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
        if hasattr(value, '__call__') and item in self._keys:
            raise Exception("Can't do that, same function name in the dataset.")
        return object.__setattr__(self, item, value)

    def __setitem__(self, item, value):
        if item in self._keys and not hasattr(value, '__call__'):
            self._keys[item] = value
            return self._keys[item]
        if hasattr(value, '__call__') and item in self._keys:
            raise Exception("Can't do that, same function name in the dataset.")
        return object.__setattr__(self, item, value)

    def __delitem__(self, item):
        if item in self._keys:
            del(self._keys[item])
        else:
            object.__delitem__(self, item)


class redisList(object):
    """
    Attempts to emulate a python list, while storing the list
    in redis.
    """
    def __init__(self, start=[], key=None, redis=db.redisBucketServer):
        if not key:
            raise Exception("Key can't be None")
        self._list = start
        self.redis = redis
        self.key = key

    def __repr__(self):
        return repr(self._list)

    def __str__(self):
        return str(self._list)

    def append(self, other):
        self._list.append(other)
        self.redis.rpush(self.key, other)
        return self._list

    def extend(self, other):
        self._list.extend(other)
        self.redis.rpush(self.key, *other)
        return self._list

    def insert(self, index, elem):
        self._list.insert(index, elem)
        self.redis.linsert(self.key, 'AFTER', index, elem)
        return self._list

    def remove(self, elem):
        self._list.remove(elem)
        self.redis.lrem(self.key, 1, elem)
        return self._list

    def pop(self):
        value = self._list.pop()
        self.redis.lpop(self.key)
        return value

    def index(self, elem):
        return self._list.index(elem)

    def count(self):
        return self._list.count()

    #def sort(self):
        #return self._list.sort()

    #def reverse(self):
        #return self._list.reverse()

    def __len__(self):
        return len(self._list)

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        self._list[index] = value
        self.redis.lset(self.key, index, value)

    def __delitem__(self, index):
        return self.remove(index)

    def __iter__(self):
        return self._list

    def __contains__(self, item):
        if item in self._list:
            return True
        return False


class redisSet(object):
    def __init__(self, start=set()):
        self._set = start

class redisSortedSet(object):
    def __init__(self):
        """
        We store the sorted list as a list of tuples where each
        tuple is (value, score)
        """
        self._set = []
