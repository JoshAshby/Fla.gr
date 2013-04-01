#!/usr/bin/env python
"""
fla.gr helper utils for mainly the redis db models
"""
def toBoolean(str):
    """
    Helper function to convert the string True of False into a boolean
    :param str: True or False as a string
    :type str: Str
    """
    if str[0] == 'T':
        return True
    else:
        return False
