#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Database model base so everything builds off this...

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

import string
import random

import models.blocks.redisBlocks.redisBlocks as rb


class baseBlockModel(object):
        def __init__(self, id=None):
                if not id:
                        self.id = u"".join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                else:
                        self.id = id
 
                self.key = "%s:%s" % (self.objectID, self.id)
                for field in self.fields:
                        fType = type(field)
                        name = field[0] if fType != str else field
                        objectKey = "%s:%s" % (self.key, name)
                        if fType == str:
                                obj = getattr(rb, "blockString")
                        else:
                                obj = getattr(rb, "block"+field[1].lower().title())
                        if fType != str and len(field) > 2:
                                value = obj(objectKey, self.dbName, field[2])
                        else:
                                value = obj(objectKey, self.dbName, unicode)
                        setattr(self, name, value)

                if not id:
                        self.new()

        def new(self):
                pass

        def commit(self):
                for field in self.fields:
                        fType = type(field)
                        name = field[0] if fType != str else field
                        block = getattr(self, name)
                        block.commit()
                key = "%s:%s" % (self.key, "id")
                idBlock = rb.blockString(key, self.dbName)
                idBlock.current = self.id
                idBlock.commit()

        def delete(self):
                for field in self.fields:
                        fType = type(field)
                        name = field[0] if fType != str else field
                        block = getattr(self, name)
                        block.delete()

                key = "%s:%s" % (self.key, "id")
                block = rb.blockString(key, self.dbName)
                block.delete()

        def __getitem__(self, item):
                return object.__getattribute__(self, item).current

        def __setitem__(self, item, value):
                item = object.__getattribute__(self, item)
                item.current = value
                return value

        def __setattr__(self, item, value):
                for field in self.fields:
                        fType = type(field)
                        name = field[0] if fType != str else field
                        if item is name:
                                try:
                                        item = object.__getattribute__(self, item)
                                        item.current = value
                                        return value
                                except:
                                        object.__setattr__(self, item, value)
                return object.__setattr__(self, item, value)

        def __str__(self):
                reply = "id: %s" % self.id
                for field in self.fields:
                        fType = type(field)
                        name = field[0] if fType != str else field
                        reply += """
        %s: %s
                        """ % (name, getattr(self, name))
                return reply

        def __repr__(self):
                reply = "id: %s" % self.id
                for field in self.fields:
                        fType = type(field)
                        name = field[0] if fType != str else field
                        reply += """
        %s: %s
                        """ % (name, getattr(self, name))
                return reply
