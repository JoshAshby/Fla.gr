#!/usr/bin/env python
"""
Database eating gator.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from gators.baseGator import baseGator
import redis
from couchdb import Server


class config(baseGator):
    baseFile = 'database.json'
    def postInit(self):
        redisURL = self._data["redisDB"]["URL"]
        for bit in self._data["redisDB"]["databases"]:
            db = self._data["redisDB"]["databases"][bit]
            self._data["redis"+bit.capitalize()+"Server"] = redis.StrictRedis(redisURL, db=db)

        self._data["couchServer"] = Server(self._data["couchDB"]["URL"]+":"+str(self._data["couchDB"]["port"]))[self._data["couchDB"]["name"]]
