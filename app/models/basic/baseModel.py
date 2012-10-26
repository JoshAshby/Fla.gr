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
import siteConfig.dbConfig as dbc
import string
import random


class baseRedisModel(object):
        def __init__(self, id=None):
                self.id = id

                if(self.id and getattr(dbc, self.__dbname__).exists(self.__dbid__+self.id)):
                        for bit in self.parts:
                                setattr(self, bit, getattr(dbc, self.__dbname__).hget(self.__dbid__+self.id, bit))
                        self.id = id
                else:
                        for bit in self.parts:
                                setattr(self, bit, None)
                        self.id = u"".join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
                        self.new()

        def new(self):
                pass

        def commit(self):
                for bit in self.parts:
                        getattr(dbc, self.__dbname__).hset(self.__dbid__+self.id, bit, getattr(self, bit))

        def __getattr__(self, item):
                return object.__getattribute__(self, item)

        def __getitem__(self, item):
                return object.__getattribute__(self, item)

        def __setattr__(self, item, value):
                return object.__setattr__(self, item, value)

        def __setitem__(self, item, value):
                return object.__setattr__(self, item, value)

        def delete(self):
                getattr(c, self.__dbname__).delete(self.__dbid__+self.id)

        def __str__(self):
                reply = ""
                for part in self.parts:
                         reply += "%s: "%(part) + getattr(self, part) + "\r\n"

                return reply

        def __repr__(self):
                reply = ""
                for part in self.parts:
                         reply += "%s: "%(part) + getattr(self, part) + "\r\n"

                return reply
