#!/usr/bin/env python
"""
Util for logging in and out
"""


class usernameError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class passwordError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class banError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
