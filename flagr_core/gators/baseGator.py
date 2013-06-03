#!/usr/bin/env python
"""
Base gator. Eat all the config!

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import os
import json


class baseGator(object):
    baseFolder = '/home/josh/repos/flagr/flagr_core'
    def __init__(self):

        siteConfigFile = self.baseFolder + '/config/' + self.baseFile
        if os.path.exists(siteConfigFile):
            siteConfigFile = open(siteConfigFile)
            siteConfig = json.loads(siteConfigFile.read())
            siteConfigFile.close()
        else:
            raise Exception("No config.json found in config/! (Aka: This is super bad.)")

        self._data = {}
        for item in siteConfig:
            data = self.preInitInsert(item, siteConfig)
            self._data[item] = data

        self.postInit()

    def preInitInsert(self, item, data):
        return data[item]

    def postInit(self):
        pass

    def _get(self, item):
        if item[0] != "_":
            data = object.__getattribute__(self, "_data")
            if item in data:
                return data[item]
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        return self._get(item)

    def __getitem__(self, item):
        return self._get(item)
