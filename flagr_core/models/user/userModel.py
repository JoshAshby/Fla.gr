#!/usr/bin/env python
"""
fla.gr user model

given a userID or a username or a email, return the users couchdb ORM

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from couchdb.mapping import Document, TextField, DateTimeField, BooleanField, IntegerField
from datetime import datetime

import config.dbBase as db
import utils.alerts as ua
import utils.sessionExceptions as use
import utils.markdownUtils as mdu

import bcrypt
import json


def findUserByID(userID):
    """
    Searches couchdb for the requested user, by the userID and returns
    a userORM object if a user is found

    :param userID: The userID to search for
    :return: The `userORM` instance if a user is found,
        `None` if no user is found
    """
    users = userORM.view(db.couchServer, 'typeViews/user', key=userID)
    if not users.rows:
        return None
    elif len(users)>1:
        raise Exception("Multiple Users")
    else:
        user = users.rows[0]
        user.formatedAbout = mdu.markClean(user.about)
        return user

def findUserByUsername(username):
    """
    Searches couchdb for documents that have the requested username

    :param username: The username to search for
    :return: The `userORM` instance if a user is found,
        `None` if no user is found
    """
    users = userORM.view(db.couchServer, 'typeViews/user')
    if not users:
        return None
    foundUser = []
    for user in users:
        if user.username == username:
            foundUser.append(user)
    if not foundUser:
        return None
    if len(foundUser)>1:
        raise Exception("Multiple Users")
    else:
        user = foundUser[0]
        user.formatedAbout = mdu.markClean(user.about)
        return user


class userORM(Document):
    username = TextField()
    email = TextField()
    about = TextField()
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
    alerts = ""
    formatedAbout = ""

    @classmethod
    def new(cls, username, password):
        """
        Make a new user, checking for username conflicts. If no conflicts are
        found the password is encrypted with bcrypt and the resulting `userORM` returned.

        :param username: The username that should be used for the new user
        :param password: The plain text password that should be used for the password.
        :return: `userORM` if the username is available,
        """
        if not findUserByUsername(username):
            passwd = bcrypt.hashpw(password, bcrypt.gensalt())
            user = cls(username=username, password=passwd)
            return user
        else:
            raise Exception("That username is taken, please choose again.")

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

    @classmethod
    def login(cls, user, password, cookieID):
        """
        Atempt to find and then log in a user, if their passwords match

        :param user: The userID or username of the user to log in
        :param password: The plain text password which the user supplies, to be checked against the found password
        :return: The `userORM` instance if a user if found and the passwords match
        """
        foundUser = findUserByID(user) or findUserByUsername(user)
        if foundUser:
            if not foundUser.disable:
                if foundUser.password == bcrypt.hashpw(password, foundUser.password):
                    db.redisSessionServer.hset(cookieID, "userID", foundUser.id)
                    user = cls.load(db.couchServer, foundUser.id)
                    user.sessionID = cookieID
                    user.loggedIn = True
                    user.alerts = db.redisSessionServer.hget(cookieID, "alerts")
                    user.store(db.couchServer)
                    return user
                else:
                    raise use.passwordError("Your password appears to be wrong.")
            else:
                raise use.banError("Your user is currently disabled. Please contact an admin for additional information.")
        raise use.usernameError("We can't find your user, are you sure you have the correct information?")

    def logout(self):
        """
        Sets the users loggedIn to False then removes the link between their
        session and their `userORM`

        :return: Nothing
        """
        self.loggedIn = False
        self.store(db.couchServer)
        db.redisSessionServer.hdel(self.sessionID, "userID")
        return True

    def saveAlerts(self):
        db.redisSessionServer.hset(self.sessionID, "alerts", json.dumps(self.alerts))
        return True

    def save(self):
        self.store(db.couchServer)
        db.redisSessionServer.hset(self.sessionID, "alerts", json.dumps(self.alerts))
        return True

    def setPassword(self, password):
        """
        Sets the users password to `password`

        :param password: plain text password to hash
        :return: `True`
        """
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.store(db.couchServer)
