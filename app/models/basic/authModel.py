#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
Database model for authentication and users

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

import bcrypt

import models.basic.baseModel as bm


def userList():
        users = []
        for key in c.redisUserServer.keys("user:*"):
                user = baseUser(key[5:])
                if user.level == "GOD" and c.session.user.level == "GOD":
                        users.append(user)
                elif user.level != "GOD":
                        users.append(user)

        return users

def findUser(username):
        users = []
        for key in c.redisUserServer.keys("user:*"):
                user = baseUser(key[5:])
                if user.username == username:
                        return user


class baseUser(bm.baseRedisModel):
        __dbname__ = "redisUserServer"
        __dbid__ = "user:"
        parts = ["username", "level", "password", "notes", "id"]

        def __setattr__(self, item, value):
                if item == "password" and value and value[:7] != "$2a$12$":
                        value = bcrypt.hashpw(value, bcrypt.gensalt())

                return object.__setattr__(self, item, value)

        def __setitem__(self, item, value):
                if item == "password" and value and value[:7] != "$2a$12$":
                        value = bcrypt.hashpw(value, bcrypt.gensalt())

                return object.__setattr__(self, item, value)
