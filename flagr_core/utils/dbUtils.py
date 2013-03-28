#!/usr/bin/env python
"""
fla.gr helper utils for mainly the redis db models
"""
def toBoolean(str):
    if str[0] == 'T':
        return True
    else:
        return False
