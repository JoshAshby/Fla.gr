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
    :return: Either a `userORM` object, if a user is found associated with a session,
        otherwise, a `dummySession` anonymous object.
    """
    #if there isn't a config setting for using dummy sessions for everything
    #then we can go ahead and make either a new dummy if anonymous
    #or pull in the userModel if there is a user logged in
    if not c.dummySession:
        userID = db.redisSessionServer.hget(cookieID, "userID")
        if userID:
            user = userModel.userORM.find(userID)
        else:
            user = dummySession(cookieID)

        #We also try to get the alerts however this might not work because
        #there might now be any json to pull in (eg: empty hash value in redis)
        try:
            user._alerts = json.loads(db.redisSessionServer.hget(cookieID, "alerts"))
        except:
            pass

        return user

    #Otherwise, use a dummy session for everything, useful for testing if you
    #want to inject a custom dummy
    else:
        dummy = dummySession()

        return dummy


class dummySession(object):
    """
    Dummy object which is made when no session could be found in redis
    Supports all the methods and attributes which are needed for fla.gr
    to run smoothly in anonymous mode. Other attributes are provided
    so the session can also be subclassed (provided the dummy session
    in the above method `session` is updated to use the subclassed dummy)
    for testing. 
    """
    def __init__(self, cookieID):
        """
        Takes a cookie stored session ID and creates a dummy session, or pulls
        in the alerts, if a session already exists.

        :param cookieID: The session ID which is stored in a cookie and sent
             to and from the browser. This is handled by Seshat and passed to
             this object through the `session` method above.
        """
        self.loggedIn = False
        self.username = ""
        self.history = ""
        self.redirect = ""
        self.sessionID = cookieID
        self.id = 0
        self.level = 0
        self._alerts = []

    def store(self, dbDummy):
        db.redisSessionServer.hset(self.sessionID, "alerts",
                json.dumps(self._alerts))

    def pushAlert(self, *args, **kwargs):
        """
        Creates an alert message to be displayed or relayed to the user,
        This is a higher level one for use in HTML templates.
        All params are of type str

        :param message: The text to be placed into the main body of the alert
        :param quip: Similar to a title, however just a quick attention getter
        :param alertType: Can be any of `success` `error` `info` `warning`
        :param expire: Currently this isn't used, however it can be set to
            anything other than next to have the alert stay permanently
        """
        self.alerts = self.HTMLAlert(*args, **kwargs);

    def saveAlerts(self):
        db.redisSessionServer.hset(self.sessionID, "alerts",
                json.dumps(self._alerts))

    @property
    def alerts(self):
        """
        Returns a str on compiled alerts, for direct placement in a template

        :return: Str of alerts
        """

        _alerts = ""
        for alert in self._alerts:
            _alerts += alert["alert"]

        return _alerts

    @alerts.setter
    def alerts(self, value):
        self._alerts.append(value)

    @alerts.deleter
    def alerts(self):
        """
        Clears the alerts for the current session. Only if the alert is set
        to expire next however, will it be cleared, allowing for persistent
        alerts.
        """

        for alert in self._alerts:
            if alert["expire"] == "next":
                self._alerts.pop(self._alerts.index(alert))

    @staticmethod
    def HTMLAlert(message, quip="", alertType="info", expire="next"):
        return {"expire": expire, "alert": ua.alert(message, quip, alertType)}

    def save(self):
        """
        Same as `store` Simply stores the sessions alerts in redis for
        the next page load from the session.
        """
        db.redisSessionServer.hset(self.sessionID, "alerts",
                json.dumps(self._alerts))

    def logout(self):
        """
        Dummy interface. Not sure if this is needed, so it may soon be removed
        """
        return False
