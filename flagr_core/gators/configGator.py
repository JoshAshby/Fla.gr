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
#from gators.baseGator import baseGator
from gators.baseGator import *


class config(baseGator):
    baseFile = 'config.json'
    def preInitInsert(self, item, data):
        if item == "dirs" or item == "files":
            for bit in data[item]:
                try:
                    data[item][bit] = data[item][bit] % self.baseFolder
                except:
                    pass
        return data[item]
