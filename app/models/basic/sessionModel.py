#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import siteConfig.dbConfig as dbc
import string
import random
import bcrypt

import models.basic.baseModel as bm

import models.profileModel as profilem


class session(bm.baseRedisModel):
        __dbname__ = "redisSessionServer"
        __dbid__ = "session:"
        parts = ["history", "userID", "messages", "loggedIn", "redirect"]

        def __init__(self, id):
                self.id = id

                if(getattr(dbc, self.__dbname__).exists(self.__dbid__+self.id)):
                        for bit in self.parts:
                                setattr(self, bit, getattr(dbc, self.__dbname__).hget(self.__dbid__+self.id, bit))

                        self.user = profilem.profile(self.userID)

                else:
                        #No session was found so make a new one
                        for bit in self.parts:
                                setattr(self, bit, None)

                        self.alerts = ""
                        self.history = ""
                        self.loggedIn = False

                        self.user = profilem.profile()

        def getAlert(self):
                returnData = self.alerts
                self.alerts = ""
                return returnData

        def pushAlert(self, message, title="", icon="pushpin", type="info"):
                content = ""
                if icon and title:
                        content += " %s"%title
                if icon and not title:
                        content += ""
                elif title and not icon:
                        content += title

                content += message

                if type:
                        self.alerts += content

        def login(self, username, passwd):
                foundUser = profilem.findUser(username)
                if foundUser:
                        if not foundUser["disable"]:
                                if foundUser["password"] == bcrypt.hashpw(passwd, foundUser["password"]):
                                        self.loggedIn = True
                                        self.user = foundUser
                                        self.userID = foundUser.id
                                else:
                                        self.logout()
                                        raise Exception("Your password appears to be wrong")

                        else:
                                self.logout()
                                raise Exception("Your user is currently disabled. Please contact an admin to determine why.")
                else:
                        self.logout()
                        raise Exception("We can't find that username, are you sure it's correct?")

        def logout(self):
                self.loggedIn = False
                self.user = None
                self.userID = None
