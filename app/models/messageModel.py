#!/usr/bin/env python2
"""


For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import models.baseMessage as bmess
import models.blocks.helpers as helpers
import markdown

def message(id=None, md=True):
        if id:
                key = id.strip("message:")
                returnPro = bmess.baseMessage(key)
                if md:
                        returnPro["message"] = markdown.markdown(returnPro["message"])
        if not id:
                returnPro = bmess.baseMessage()

        return returnPro


class mail(object):
        def __init__(self, userID=None):
                id = c.session.userID if c.session else None
                self.userID = userID if userID else id
                self.messages = []

                keys = c.redisUserServer.keys("message:*:id")
                for key in keys:
                        if c.redisUserServer.get(key.strip(":id")+":user") == self.userID:
                                self.messages.append(message(key))

        def unreadCount(self):
                count = 0
                for message in self.messages:
                        if not message["read"] and not message["archive"]:
                                count += 1
                return count

        def readCount(self):
                count = 0
                for message in self.messages:
                        if message["read"] and not message["archive"]:
                                count += 1
                return count
