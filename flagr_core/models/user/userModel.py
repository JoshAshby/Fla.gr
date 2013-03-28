#!/usr/bin/env python
"""
fla.gr user model

Given a userID or a username or a email, return the users couchdb ORM

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com

>>> import models.user.userModel as um
>>> import bcrypt
"""

from couchdb.mapping import Document, TextField, DateTimeField, \
        BooleanField, IntegerField
import bcrypt
import json
from datetime import datetime

import config.dbBase as db
import utils.alerts as ua
import utils.sessionExceptions as use
import utils.markdownUtils as mdu

from models.modelExceptions.userModelExceptions import \
       multipleUsersError, passwordError, userError

from models.baseModel import baseCouchModel


class userORM(Document, baseCouchModel):
    """
    Base ORM for users in fla.gr, this one currently uses couchdb to store
    the data.
    TODO: Flesh this doc out a lot more
    """
    username = TextField()
    email = TextField()
    about = TextField(default="")
    disable = BooleanField(default=False)
    emailVisibility = BooleanField(default=False)
    history = TextField()
    level = IntegerField(default=1)
    loggedIn = BooleanField(default=False)
    redirect = BooleanField(default=False)
    password = TextField()
    joined = DateTimeField(default=datetime.now)
    sessionID = TextField()
    docType = TextField(default="user")
    alerts = []
    _view = 'typeViews/user'

    @classmethod
    def new(cls, username, password):
        """
        Make a new user, checking for username conflicts. If no conflicts are
        found the password is encrypted with bcrypt and the resulting `userORM` returned.

        >>> password = "test"
        >>> username = "Test"
        >>> newUser = um.userORM.new(username, password)
        >>> newUser # doctest: +ELLIPSIS
        <userORM ...>
        >>> assert newUser.password == bcrypt.hashpw(password, newUser.password)
        >>> assert newUser.username == username

        :param username: The username that should be used for the new user
        :param password: The plain text password that should be used for the password.
        :return: `userORM` if the username is available
        """
        if password == "":
            raise passwordError("Password can not be null")
        elif not cls.find(username):
            passwd = bcrypt.hashpw(password, bcrypt.gensalt())
            user = cls(username=username, password=passwd)
            return user
        else:
            raise userError("That username is taken, please choose again.",
                    username)

    def setPassword(self, password):
        """
        Sets the users password to `password`

        :param password: plain text password to hash
        """
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.store(db.couchServer)

    @classmethod
    def login(cls, user, password, cookieID):
        """
        Attempt to find and then log in a user, if their passwords match

        :param user: The userID or username of the user to log in
        :param password: The plain text password which the user supplies, \
                to be checked against the found password
        :return: The `userORM` instance if a user if found and the passwords \
                match. Raises an exception if the password, or username are
                wrong, or if the user has been disabled.
        """
        foundUser = cls.find(user)
        if foundUser:
            if not foundUser.disable:
                if foundUser.password == bcrypt.hashpw(password,
                        foundUser.password):
                    db.redisSessionServer.hset(cookieID, "userID",
                            foundUser.id)
                    user = cls.load(db.couchServer, foundUser.id)
                    user.sessionID = cookieID
                    user.loggedIn = True
                    user.alerts = db.redisSessionServer.hget(cookieID,
                            "alerts")
                    user.save()
                    return user
                else:
                    raise use.passwordError("Your password appears to \
                            be wrong.")
            else:
                raise use.banError("Your user is currently disabled. \
                        Please contact an admin for additional information.")
        raise use.usernameError("We can't find your user, are you \
                sure you have the correct information?")

    def loginThis(self, cookieID):
        """
        Kind of like above, however this one logs in a user.
        No password checking or usernames to find, just pass
        the cookieID and they're set.
        For example: when finishing registering, the user can be logged in
        without having to go through the log in process...

        :param cookieID: The sessions cookie ID for the person to login
        """
        db.redisSessionServer.hset(cookieID, "userID", self.id)
        self.sessionID = cookieID
        self.loggedIn = True
        self.alerts = db.redisSessionServer.hget(cookieID, "alerts")
        self.save()

    def logout(self):
        """
        Sets the users loggedIn to False then removes the link between their
        session and their `userORM`
        """
        self.loggedIn = False
        self.store(db.couchServer)
        db.redisSessionServer.hdel(self.sessionID, "userID")
        return True

    def clearAlerts(self):
        """
        Clears the current users expired alerts.
        """
        for alert in self.alerts:
            if alert["expire"] == "next":
                self.alerts.pop(self.alerts.index(alert))

    def pushAlert(self, message, quip="", alertType="info", expire="next"):
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
        self.alerts.append({"expire": expire,
            "alert": ua.alert(message, quip, alertType)})

    def getAlerts(self):
        """
        Returns a str on compiled alerts, for direct placement in a template

        :return: Str of alerts
        """
        alerts = ""
        for alert in self.alerts:
            alerts += alert["alert"]

        return alerts

    def saveAlerts(self):
        """
        Saves the current users alerts and places them into redis
        """
        db.redisSessionServer.hset(self.sessionID, "alerts",
                json.dumps(self.alerts))

    @staticmethod
    def _search(items, value):
        """
        Searches the list `items` for the given value

        :param items: A list of ORM objects to search
        :param value: The value to search for, in this case
            value can be a username or an email, or an id
        """
        foundUser = []
        for user in items:
            if user.email == value or user.username == value or user.id == value:
                foundUser.append(user)
        if not foundUser:
            return None
        if len(foundUser)>1:
            raise multipleUsersError("Multiple Users", value)
        else:
            user = foundUser[0]
            user.formatedAbout = mdu.markClean(user.about)
            return user

    def save(self):
        """
        Override of the baseCouchModel method: save
        Saves the user object, along with saving the alerts to redis
        """
        #self.store(db.couchServer)
        super(baseCouchModel, self).save()
        db.redisSessionServer.hset(self.sessionID, "alerts",
                json.dumps(self.alerts))
