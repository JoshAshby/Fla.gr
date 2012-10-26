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


class blockString(object):
        def __init__(self, key, dbName, dataType=unicode):
                self.dbName = dbName
                self.dataType=dataType
                self.key = key


                if getattr(dbc, self.dbName).exists(self.key):
                        self.current = dataType(getattr(dbc, self.dbName).get(self.key))
                else:
                        self.current = dataType(u"")

        def commit(self):
                getattr(dbc, self.dbName).set(self.key, self.current)

        def delete(self):
                getattr(dbc, self.dbName).delete(self.key)

        def __str__(self):
                reply = u"%s" % self.current
                return reply

        def __repr__(self):
                reply = u"%s" % self.current
                return reply
