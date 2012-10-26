#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Helper stuff for bits of data...

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""

def boolean(bit):
        try:
                return {"True": True, "true": True, "1": True, 1: True, "on": True, True: True, "False": False, "false": False, "0": False, 0: False, "off": False, False:False}[bit]
        except:
                return bool(bit)


def strToList(bit):
        if bit == "None":
                return []
        elif not bit:
                return []
        else:
                return bit.replace("'", "").replace(" ", "").split(",")
