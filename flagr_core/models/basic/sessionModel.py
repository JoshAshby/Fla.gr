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
            user = userModel.userORM.find(userID)
        else:
            user = dummySession(cookieID)

        try:
            user._alerts = json.loads(db.redisSessionServer.hget(cookieID, "alerts"))
        except:
            pass

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
        self.id = 0
        self.level = 0
        self._alerts = []


    def store(self, dbDummy):
        db.redisSessionServer.hset(self.sessionID, "alerts", json.dumps(self._alerts))

    def pushAlert(self, *args, **kwargs):
        self.alerts = self.HTMLAlert(*args, **kwargs);

    def saveAlerts(self):
        db.redisSessionServer.hset(self.sessionID, "alerts", json.dumps(self._alerts))
        return True

    @property
    def alerts(self):
        _alerts = ""
        for alert in self._alerts:
            _alerts += alert["alert"]

        return _alerts

    @alerts.setter
    def alerts(self, value):
        self._alerts.append(value)

    @alerts.deleter
    def alerts(self):
        for alert in self._alerts:
            if alert["expire"] == "next":
                self._alerts.pop(self._alerts.index(alert))

    @staticmethod
    def HTMLAlert(message, quip="", alertType="info", expire="next"):
        return {"expire": expire, "alert": ua.alert(message, quip, alertType)}

    def save(self):
        db.redisSessionServer.hset(self.sessionID, "alerts", json.dumps(self._alerts))

    def logout(self):
        return False
