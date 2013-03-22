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
import utils.alerts as ua
import json


def session(cookieID):
    """
    Attempt to make a user to the current session, returning the `userORM` if one is found.

    :param cookieID: The session id, taken from the browsers cookie data.
    :return: Either a `userORM` object, if a user is found asscoiated with a session,
        otherwise, a `dummySession` anonymous object.
    """
    if not c.dummySession:
        userID = db.redisSessionServer.hget(cookieID, "userID")
        if userID:
            user = userModel.findUserByID(userID)
        else:
            user = dummySession(cookieID)

        try:
            user.alerts = json.loads(db.redisSessionServer.hget(cookieID, "alerts"))
        except:
            user.alerts = []

        return user

    else:
        dummy = dummySession()

        return dummy


class dummySession(object):
    def __init__(self, cookieID):
        self.loggedIn = False
        self.username = ""
        self.history = ""
        self.redirect = ""
        self.sessionID = cookieID
        self.alerts = []
        self.id = 0
        self.level = 0
        self.alerts = []

    def clearAlerts(self):
        for alert in self.alerts:
            if alert["expire"] == "next":
                self.alerts.pop(self.alerts.index(alert))

    def pushAlert(self, message, quip="", alertType="info", expire="next"):
        self.alerts.append({"expire": expire, "alert": ua.alert(message, quip, alertType)})

    def getAlerts(self):
        alerts = ""
        for alert in self.alerts:
            alerts += alert["alert"]

        return alerts

    def store(self, dbDummy):
        db.redisSessionServer.hset(self.sessionID, "alerts", json.dumps(self.alerts))

    def saveAlerts(self):
        db.redisSessionServer.hset(self.sessionID, "alerts", json.dumps(self.alerts))
        return True

    def save(self):
        db.redisSessionServer.hset(self.sessionID, "alerts", json.dumps(self.alerts))

    def logout(self):
        return False
