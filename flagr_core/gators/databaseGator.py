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
    _temp = {}
    def preInitInsert(self, item, data):
        if item == "redisDB":
            if data[item]["storeSeparate"]:
                for bit in data[item]["databases"]:
                    self._temp["redis"+bit.capitalize()+"Server"] = redis.StrictRedis(data[item]["URL"], db=data[item]["databases"][bit])
            else:
                self._temp["redis"] = redis.StrictRedis(data[item]["URL"], db=data[item]["db"])
        if item == "couchDB":
            serv = None
            try:
                serv = Server(data[item]["URL"]+":"+str(data[item]["port"]))[data[item]["name"]]
            except Exception as exc:
                print exc
            self._temp["couchServer"] = serv
        return data[item]

    def postInit(self):
        self._data = self._temp
