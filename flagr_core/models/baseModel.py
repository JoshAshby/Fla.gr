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

class redisKeysBase(object):
    def __init__(self, key, redis=db.redisBucketServer):
        object.__setattr__(self, "_data", dict())
        self.redis = redis
        self.key = key+":"

    def __getattr__(self, item):
        if item in object.__getattribute__(self, "_data"):
            return object.__getattribute__(self, "_data")[item]
        return object.__getattribute__(self, item)

    def __getitem__(self, item):
        if item in object.__getattribute__(self, "_data"):
            return object.__getattribute__(self, "_data")[item]
        return object.__getattribute__(self, item)

    def __setattr__(self, item, value):
        data = object.__getattribute__(self, "_data")
        if item in data and not hasattr(value, '__call__'):
            data[item] = value
            self.redis.set(self.key+item, value)
        if hasattr(value, '__call__') and item in self._data:
            raise Exception("Can't do that, same function name in the dataset.")
        return object.__setattr__(self, item, value)

    def __setitem__(self, item, value):
        data = object.__getattribute__(self, "_data")
        if item in data and not hasattr(value, '__call__'):
            data[item] = value
            self.redis.set(self.key+item, value)
        if hasattr(value, '__call__') and item in self._data:
            raise Exception("Can't do that, same function name in the dataset.")
        return object.__setattr__(self, item, value)

    def __delitem__(self, item):
        data = object.__getattribute__(self, "_data")
        if item in data:
            del(data[item])
            self.redis.delete(self.key+item)
        else:
            object.__delitem__(self, item)


class redisObject(object):
    """
    I said I never would, but this is another attempt at making
    an ORM for redis...
    It's probably not going to work, but heres hopping.
    """
    def __init__(self, key, redis=db.redisBucketServer, **kwargs):
        object.__setattr__(self, "_keys", redisKeysBase(key))
        self.redis = redis
        if not kwargs:
            bits = self.redis.keys("%s:*"%(key))
            if bits:
                for bit in bits:
                    objectPart = bit.strip(":"%(key))
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
        else:
            raise Exception("here")
            self.updateData(**kwargs)

    def updateData(self, *args, **kwargs):
        if kwargs:
            for kw in kwargs:
                if type(kwargs[kw]) == list:
                    key = self.key + kw
                    self._keys[kw] = redisList(key, kwargs[kw])
                elif type(kwargs[kw]) == str:
                    self._keys[kw] = kwargs[kw]
        elif args:
            if type(args[1]) == list:
                key = self.key + args[0]
                self._keys[args[0]] = redisList(key, args[1])
            elif type(args[1]) == str:
                self._keys[args[0]] = args[1]

    def __getattr__(self, item):
        keys = object.__getattribute__(self, "_keys")
        if item in keys:
            return keys[item]
        return object.__getattribute__(self, item)

    def __getitem__(self, item):
        keys = object.__getattribute__(self, "_keys")
        if item in keys:
            return keys[item]
        return object.__getattribute__(self, item)

    def __setattr__(self, item, value):
        keys = object.__getattribute__(self, "_keys")
        if item in keys and not hasattr(value, '__call__'):
            return self.updateData(item, value)
        if hasattr(value, '__call__') and item in keys:
            raise Exception("Can't do that, same function name in the dataset.")
        return object.__setattr__(self, item, value)

    def __setitem__(self, item, value):
        keys = object.__getattribute__(self, "_keys")
        if item in keys and not hasattr(value, '__call__'):
            return self.updateData(item, value)
        if hasattr(value, '__call__') and item in keys:
            raise Exception("Can't do that, same function name in the dataset.")
        return object.__setattr__(self, item, value)

    def __delitem__(self, item):
        keys = object.__getattribute__(self, "_keys")
        if item in keys:
            del(keys[item])
        else:
            object.__delitem__(self, item)


class redisList(object):
    """
    Attempts to emulate a python list, while storing the list
    in redis.
    """
    def __init__(self, key, start=[], redis=db.redisBucketServer):
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
