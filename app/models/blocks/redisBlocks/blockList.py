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

import string
import random


class blockSet(object):
        def __init__(self, id, keyID, dbName, dataType=str):
                self.id = id

                if(self.id and getattr(c, self.dbName).exists(self.keyID+self.id)):
                        list = [ dataType(i) for i in getattr(c, self.dbName).smembers(self.keyID+self.id) ]
                        self.current = list
                else:
                        self.current = list()

        def commit(self):
                for bit in self.current:
                        getattr(c, self.dbName).rpush(self.keyID+self.id, bit)
