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


class blockHash(object):
        def __init__(self, id, keyID, dbName, dataType=str, parts):
                self.id = id
                self.keyID = keyID
                self.dbName = dbName
                self.dataType = dataType
                self.parts = parts

                if(self.id and getattr(dbc, self.dbName).exists(self.keyID+self.id)):
                        self.current = { bit: dataType(getattr(dbc, self.dbName).hget(self.keyID+self.id, bit)) for bit in self.parts }
                else:
                        self.current = { bit: dataType(u"") for bit in self.parts }

        def commit(self):
                for bit in self.parts:
                        getattr(dbc, self.dbName).hset(self.keyID+self.id, bit, self.parts[bit])
