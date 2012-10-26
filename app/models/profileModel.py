#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import siteConfig.dbConfig as dbc
import models.baseProfile as bpro
import models.blocks.helpers as helpers
import markdown

def profile(userID=None, md=True):
        if userID:
                key = userID.strip("profile:")
                returnPro = bpro.baseProfile(key)
                if md:
                        returnPro["about"] = markdown.markdown(returnPro["about"])
        if not userID:
                returnPro = bpro.baseProfile()

        return returnPro

def userList():
        users = []
        for key in dbc.redisUserServer.keys("profile:*:id"):
                if dbc.redisUserServer.get(key.strip(":id")+":level") == "GOD" and dbc.session.user["level"] != "GOD":
                        pass
                else:
                        user = profile(key.strip(":id"))
                        users.append(user)

        return users

def findUser(username):
        for key in dbc.redisUserServer.keys("profile:*:username"):
                if dbc.redisUserServer.get(key) == username:
                        user = profile(key.strip(":username"))
                        return user
