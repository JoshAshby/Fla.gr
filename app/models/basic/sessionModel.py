#!/usr/bin/env python2
"""
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
import string
import random
import bcrypt

import models.basic.baseModel as bm
import views.pyStrap.pyStrap as ps

import models.profileModel as profilem
import models.messageModel as mm


class session(bm.baseRedisModel):
        __dbname__ = "redisSessionServer"
        __dbid__ = "session:"
        parts = ["history", "userID", "messages", "loggedIn", "redirect"]

        def __init__(self, id):
                self.id = id

                if(getattr(c, self.__dbname__).exists(self.__dbid__+self.id)):
                        for bit in self.parts:
                                setattr(self, bit, getattr(c, self.__dbname__).hget(self.__dbid__+self.id, bit))

                        self.user = profilem.profile(self.userID)
                        self.mail = mm.mail(self.userID)

                else:
                        #No session was found so make a new one
                        for bit in self.parts:
                                setattr(self, bit, None)

                        self.messages = ""
                        self.history = ""
                        self.loggedIn = False

                        self.user = profilem.profile()
                        self.mail = mm.mail()

        def getMessages(self):
                returnData = self.messages
                self.messages = ""
                return returnData

        def pushMessage(self, message, title="", icon="pushpin", type="info"):
                content = ""
                if icon and title:
                        content += ps.baseHeading(ps.baseIcon(icon)+ " %s"%title, size=4)
                if icon and not title:
                        content += ps.baseIcon(icon)
                elif title and not icon:
                        content += ps.baseHeading(title, size=4)

                content += ps.baseParagraph(message)

                if type:
                        self.messages += ps.baseAlert(content, classes="alert-%s alert-block"%type)

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
                self.mail = None
