#!/usr/bin/env python
"""
fla.gr session model

Basically what we have is a key value store in redis
of all the session ID's (store and retrieved via the cookie
from Seshat)

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import models.user.userModel as userModel
import config.config as c
import config.dbBase as db

def session(cookieID):
    """
    Attempt to make a user to the current session, returning the `userORM` if one is found.

    :param cookieID: The session id, taken from the browsers cookie data.
    :return: Either a `userORM` object, if a user is found asscoiated with a session,
        otherwise, a `dummySession` anonymous object.
    """
    if not c.dummySession:
        userID = db.redisSessionServer.hget(cookieID, "userID")
        user = userModel.findUserByID(userID)
        if user:
            return user
        else:
            user = dummySession(cookieID)
            user.alerts = db.redisSessionServer.hget(cookieID, "alerts")
            return user
    else:
        dummy = dummySession()

        return dummy


class dummySession(object):
    def __init__(self, cookieID):
        self.loggedIn = False
        self.username = ""
        self.alerts = ""
        self.history = ""
        self.redirect = ""
        self.sessionID = cookieID

    def clearAlerts(self):
        self.alerts = ""

    def pushAlert(self, message):
        self.alerts = message

    def getAlerts(self):
        return self.alerts

    def store(self, dbDummy):
        db.redisSessionServer.hset(self.sessionID, "alerts", self.alerts)
