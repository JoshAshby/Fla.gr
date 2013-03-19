#!/usr/bin/env python
"""
fla.gr helper utils for mainly the redis db models

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""

def toBoolean(str):
    if str[0] == 'T':
        return True
    else:
        return False
