#!/usr/bin/env python2
"""
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


class blockString(object):
        def __init__(self, key, dbName, dataType=unicode):
                self.dbName = dbName
                self.dataType=dataType
                self.key = key


                if getattr(c, self.dbName).exists(self.key):
                        self.current = dataType(getattr(c, self.dbName).get(self.key))
                else:
                        self.current = dataType(u"")

        def commit(self):
                getattr(c, self.dbName).set(self.key, self.current)

        def delete(self):
                getattr(c, self.dbName).delete(self.key)

        def __str__(self):
                reply = u"%s" % self.current
                return reply

        def __repr__(self):
                reply = u"%s" % self.current
                return reply
