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


class blockSet(object):
        def __init__(self, key, dbName, dataType=unicode):
                self.dbName = dbName
                self.dataType=dataType
                self.key = key


                if getattr(dbc, self.dbName).exists(self.key):
                        members = getattr(dbc, self.dbName).smembers(self.key)
                        self.current = { dataType(i) for i in members }
                        self.previous = self.current
                else:
                        self.current = set()
                        self.previous = set()

        def commit(self):
                for bit in self.previous.difference(self.current):
                        getattr(dbc, self.dbName).srem(self.key, bit)

                for bit in self.current:
                        getattr(dbc, self.dbName).sadd(self.key, bit)

        def delete(self):
                getattr(dbc, self.dbName).delete(self.key)

        def __str__(self):
                reply = u""
                for bit in self.current:
                        reply += u"%s, " % bit
                reply = reply.strip(", ")
                return reply

        def __repr__(self):
                reply = u"%s" % self.current
                return reply
